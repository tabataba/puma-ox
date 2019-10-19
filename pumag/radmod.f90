      module radmod
      use pumamod

      implicit none

!     **************
!     * parameters *
!     **************
      integer, parameter :: radnl_u = 20

!     *************
!     * filenames *
!     *************
      character(256) :: rad_output = "rad_output"
      character(256) :: rad_namelist = "rad_namelist"

!     ***********************
!     * namelist parameters *
!     ***********************
      real    :: gsol0   =  SOLCON_EARTH ! stellar constant [W/m^2] 
      real    :: tsol0   =  TSOL0_SUN    ! effective stellar temp. [Kelvin] 
      real    :: dsolp0  =  DSOLP0_EARTH ! mean distance between star and
!                                        ! planet [m]
      real    :: rsol0   =  RSOL0_SUN    ! mean radius of the star [m]
      real    :: obliq   =  OBLIQ_EARTH  ! planetary obliquity [deg]
!      real    :: taus0   =  0.21         ! total shortwave optical depth at reference pressure level  
      real    :: taus0   =  0.00
      real    :: taul0   =  1.03         ! total longwave optical depth at reference pressure level
      real    :: albbnd  =  ALBBND_EARTH ! Bond albedo 
      real    :: albsfc  =  ALBSFC_EARTH ! surface shortwave albedo
      real    :: emisfc  =  EMISFC_EARTH ! surface longwave emissivity


      real    :: pref    = PREF_EARTH    ! planetary reference pressure [Pa]

!     **********
!     * arrays *
!     **********

      real, allocatable :: gmu0(:)    ! average cosine of solar zenith angle 
!      real, allocatable :: dgtsurf(:) ! surface temperature [K]
      real, allocatable :: dgtrad(:)  ! placeholder surf temp
      real, allocatable :: logcoef(:) ! coefficients for log interpolation
      end module radmod

!     =================
!     SUBROUTINE RADINI 
!     =================

      subroutine radini
      use radmod

      implicit none
     
!      real, allocatable :: gcos(:)       ! cosine of the latitude 
!      real, allocatable :: gtan(:)       ! tangent of the latitude 

      if (mypid == NROOT) then
        write(nud,  '("*====================*")')
        write(nud,  '("* RADMOD INITIALIZED *")')
        write(nud,  '("*====================*")')
      endif


!     set filenames for multirun mode
      call setradfnames

!     read radpar nameslist
      call read_radnl

!     allocate fields 
      call allocate_rad

!     calculate gmu0
      call calc_gmu0

!     calculate coefficients for logarithmic interpolation
      call interpini


      return
      end subroutine radini

!     ==================
!     SUBROUTINE RADSTEP 
!     ==================

      subroutine radstep
      use radmod


      implicit none

      call radtrans

      return
      end subroutine radstep 

!     ==================
!     SUBROUTINE RADSTOP 
!     ==================

      subroutine radstop
      use radmod

      implicit none

      if (mypid == NROOT) then
        write(nud,  '("*================*")')
        write(nud,  '("* RADMOD STOPPED *")')
        write(nud,  '("*================*")')
      endif
      return

      end subroutine radstop


!     =================
!     SUBROUTINE READNL
!     =================

      subroutine read_radnl
      use radmod

      implicit none

      logical :: lexist
      integer :: ios


!     define namelist
      namelist /radpar/ &
       gsol0   , tsol0  , dsolp0 , obliq, rsol0 , taus0 , taul0 &
      , albbnd , albsfc , emisfc 


!     inquire for and read namelist
      if (mypid == NROOT) then
        inquire(file=rad_namelist,exist=lexist)
        if (lexist) then
          open(radnl_u,file=rad_namelist,iostat=ios)
          if (ios == 0) then
            read (radnl_u,radpar)
            close(radnl_u)
          endif
        endif
        if (nrad > 0) then
          write(nud,radpar)
        endif
      endif


!     broadcast real scalars 
      call mpbcr(gsol0)
      call mpbcr(tsol0)
      call mpbcr(dsolp0)
      call mpbcr(obliq) 
      call mpbcr(rsol0) 
      call mpbcr(taus0)
      call mpbcr(taul0)
      call mpbcr(albbnd) 
      call mpbcr(albsfc)
      call mpbcr(emisfc)
      call mpbcr(pref)

      return
      end subroutine read_radnl

!     ========================
!     SUBROUTINE SETRADFNAMES
!     ========================

      subroutine setradfnames
      use radmod

      implicit none

      character (3) :: mrext

      if (mrpid <  0) return ! no multirun

      write(mrext,'("_",i2.2)') mrpid

      rad_namelist         = trim(rad_namelist        ) // mrext
      rad_output           = trim(rad_output          ) // mrext

      return
      end subroutine setradfnames


!     =======================
!     SUBROUTINE ALLOCATE_RAD
!     =======================
      subroutine allocate_rad
      use radmod

      implicit none
  
!     gridpoint arrays
      allocate(gmu0(nhor))        ! cos of solar zenith angle
!      allocate(dgtsurf(nhor))     ! surface temperature [K]
      allocate(logcoef(nlem))     ! coefficients for log interpolation
      allocate(dgtrad(nhor))      ! placeholder for surface temp
!      allocate(gcos(nhor))
!      allocate(gtan(nhor))
!      dgtsurf(:) = 288.0
      dgtrad(:) = 0.0
      return
      end subroutine allocate_rad

!     ====================
!     SUBROUTINE CALC_GMU0
!     ====================
      subroutine calc_gmu0
      use radmod

      implicit none

      real ::  gcos(nhor) 
      real ::  gtan(nhor)

      integer,parameter :: ntac = 360
      integer :: itac,jhor

      real ::  dcl(ntac),hfdl(nhor,ntac),csz(nhor,ntac)
      real ::  insod(nhor,ntac),insot(nhor)

      gcos(:) = sqrt(1-gsinalt(:)*gsinalt(:))
      gtan(:) = gsinalt(:)/gcos(:)


      obliq = obliq * PI/180.0

      do itac = 1, ntac
	dcl(itac) = -obliq * cos(2*PI*itac/ntac)
      enddo
      
      do jhor = 1, nhor
        insot(jhor) = 0.0	
        do itac = 1, ntac
	  if (abs(gtan(jhor)*tan(dcl(itac))) .lt. 1.0) then
	    hfdl(jhor,itac) = acos(-gtan(jhor)*tan(dcl(itac)))
	    csz(jhor,itac) = gsinalt(jhor)*sin(dcl(itac)) &
                           + gcos(jhor)*cos(dcl(itac)) &
                           *sin(hfdl(jhor,itac))/hfdl(jhor,itac)
 	  else if (gtan(jhor)*tan(dcl(itac)) .ge. 1.0) then
	    hfdl(jhor,itac) = PI
	    csz(jhor,itac) = gsinalt(jhor)*sin(dcl(itac))
          else if (gtan(jhor)*tan(dcl(itac)) .le. -1.0) then
            hfdl(jhor,itac) = 0.0
            csz(jhor,itac) = 0.0
          endif
          insod(jhor,itac) = gsol0/PI * csz(jhor,itac) * hfdl(jhor,itac)
          insot(jhor) = insot(jhor) + insod(jhor,itac)
        enddo
	gmu0(jhor) = (insot(jhor)/ntac)*1.0/gsol0
      enddo

      return
      end subroutine calc_gmu0

!     ====================
!     SUBROUTINE INTERPINI
!     ====================
      subroutine interpini
      use radmod

      implicit none

      integer jlev

      do jlev=1,nlem  
!        logcoef(jlev) = log(sigmh(jlev+1)/sigma(jlev)) &
!                        * log(sigmh(jlev+1)/sigmh(jlev)) 
         logcoef(jlev) = log(sigmh(jlev+1)/sigmh(jlev))/log(sigmh(jlev+1)/sigma(jlev))
      enddo

      return
      end subroutine interpini


!     ===================
!     SUBROUTINE RADTRANS
!     ===================
      subroutine radtrans 
      use radmod

      implicit none

!     integers      
      integer :: jlev      
      integer :: jhor


!     real  arrays 
      real ::  ztaus(nhor,nlev)     ! shortwave optical thickness
      real ::  ztaul(nhor,nlep)     ! longwave optical thickness


!     dimensional arrays
      real ::  zdgp(nhor)           ! surface pressure [Pa]
      real ::  zzdgp(nugp)
      real ::  zdgpsig(nhor,nlev)   ! pressure on sigma levels [Pa]
      real ::  zdgpsigh(nhor,nlep)  ! pressre on simga half levels [Pa]
      real ::  zdgt(nhor,nlev)      ! temperature on sigma levels [K] 
      real ::  zzdgt(nugp,nlev)
      real ::  zdgth(nhor,nlep)     ! temperature on sigma half-levels [K]
      real ::  zdgsc(nhor,nlep)     ! LW source function on sigma levels [W m^-2]
      real ::  zdgsch(nhor,0:nlep)  ! LW source function on sigma half-levels [W m^-2]
      real ::  zdgscg(nhor)         ! LW source function for ground [W m^-2]
      real ::  Uradis(nhor,nlep)    ! upward irradiance on sigma half-levels for SW [W m^-2]
      real ::  Dradis(nhor,nlep)    ! downward irradiance on sigma half-levels for SW [W m^-2]
      real ::  fnets(nhor,nlep)     ! net downward irradiance on sigma half-levels for SW [W m^-2]
      real ::  zhtrs(nhor,nlev)     ! SW heating rate [K s^-1]
      real ::  Uradil(nhor,0:nlep)  ! upward irradiance on sigma half-levels for LW [W m^-2]
      real ::  Dradil(nhor,0:nlep)  ! downward irradiance on sigma half-levels for LW [W m^-2]
      real ::  EU0(nhor), EU1(nhor), EU2(nhor)
      real ::  ED0(nhor), ED1(nhor), ED2(nhor)
      real ::  bb(nhor), bt(nhor), bl(nhor)
      real ::  fnetl(nhor,nlep)     ! net downward irradiance on sigma half-levels for LW [W m^-2]
      real ::  zhtrl(nhor,nlev)     ! LW heating rate [K s^-1]
      real ::  diffcoef(nhor,nlep)  ! coefficient for diffuse approximation

      real ::  zfgtt(nugp,nlev)
      real ::  zdgtsurf(nugp)
      real ::  epsilon_r = 1.E-5
      real ::  lwcnst1(nhor),lwcnst2(nhor)
      real ::  lwflag1(nhor),lwflag2(nhor),lwflag3(nhor),lwflag4(nhor)

!     =============================
!     produce dimensional variables 
!     =============================
     
      if (mod(nstep,ntrad)==0) then
!     surface pressure
      zdgp(:) = exp(gp(:))     ! non-dimensional surface pressure (gp = Ln(ps))
      zdgp(:) = zdgp(:)*psmean ! dimensional surface pressure in [Pa]

!     alternative Gaussian grid to regular Gaussian grid
!      call alt2reg(zdgp,1)

     qrad_int(:)=0.0

!     pressure on sigma levels and sigma half-levels
      do jlev = 1,nlem         
        zdgpsig(:,jlev)  = zdgp(:)*sigma(jlev)
        zdgpsigh(:,jlev+1) = zdgp(:)*sigmh(jlev)
      enddo
      zdgpsig(:,nlev) = zdgp(:)*sigma(nlev)
      zdgpsigh(:,1) = 0.0
      zdgpsigh(:,nlep) = zdgp(:)

!     temperature and source function on sigma levels
      do jhor = 1,nhor
        zdgt(jhor,:) = (gt(jhor,:) + t0(:))*CT
      enddo
!      call alt2reg(zdgt,nlev)
      do jlev = 1,nlev
        zdgsc(:,jlev+1) = SBC * zdgt(:,jlev)**4 
      enddo
      zdgsc(:,1) = SBC * (0.5*zdgt(:,1))**4


!     temperature and source function on sigma half-levels
      zdgth(:,nlep) = zdgt(:,nlev)
      do jlev = nlev,2,-1 
        zdgth(:,jlev) = zdgth(:,jlev+1) -    & 
                        (zdgth(:,jlev+1) - zdgt(:,jlev-1)) * logcoef(jlev-1)
      enddo
      zdgth(:,1) = zdgt(:,1)

!      zdgsch(:,0) = 0.0
      zdgsch(:,0) = SBC * (3.0)**4
      do jlev = 1,nlep
        zdgsch(:,jlev) = SBC * zdgth(:,jlev)**4
      enddo
 
      zdgscg(:) = SBC * dgtsurf(:)**4 ! dgtsurf is updated every timestep


!     ===========================
!     calculate optical thickness 
!     ===========================
      ztaus(:,1) = taus0 * zdgp(:)/pref * sigmh(1)
      ztaul(:,1) = 0.0
      ztaul(:,2) = taul0 * zdgp(:)/pref * sigmh(1)
      do jlev = 2, nlev
	ztaus(:,jlev) = taus0 * zdgp(:)/pref * (sigmh(jlev)-sigmh(jlev-1))
        ztaul(:,jlev+1) = taul0 * zdgp(:)/pref * (sigmh(jlev)-sigmh(jlev-1))
      enddo

!     ===========
!     SW transfer
!     ===========
      Dradis(:,1) = gsol0 * (1-albbnd) * gmu0(:)
! commented by Yixiong 22/11/2012
      dswtoa(:) = Dradis(:,1)

      do jlev = 2, nlep
!        Dradis(:,jlev) = Dradis(:,jlev-1) * exp(-ztaus(:,jlev-1)/gmu0(:))
        Dradis(:,jlev) = Dradis(:,jlev-1) * exp(-ztaus(:,jlev-1))
      enddo
!      Uradis(:,nlep) = Dradis(:,nlep) * albsfc
      Uradis(:,nlep) = Dradis(:,nlep) * 0.0
      do jlev = nlev, 1, -1
!        Uradis(:,jlev) = Uradis(:,jlev+1) * exp(-ztaus(:,jlev)/gmu0(:))
        Uradis(:,jlev) = Uradis(:,jlev+1) * exp(-ztaus(:,jlev))
      enddo
      do jlev = 1, nlep
        fnets(:,jlev) = Dradis(:,jlev) - Uradis(:,jlev)
      enddo

      do jlev = 1, nlev
        zhtrs(:,jlev) = ga/(gascon/akap) * (fnets(:,jlev)-fnets(:,jlev+1)) &
                        / (zdgpsigh(:,jlev+1)-zdgpsigh(:,jlev))
      enddo


      

!     ===========
!     LW transfer
!     ===========
      Dradil(:,0) = 0.0
      do jlev = 1, nlep
 	ED0(:) = 0.0
        ED1(:) = 0.0
	ED2(:) = 0.0
        diffcoef(:,jlev)=(1./(1.5 + 0.5/(1.0 + & 
                         4.0*ztaul(:,jlev) + 10.0*ztaul(:,jlev)**2)))
        bb(:) = zdgsch(:,jlev-1)
	bt(:) = zdgsch(:,jlev)
        bl(:) = zdgsc(:,jlev)
        if (bb(1).eq.0.0) then
          ED1(:) = 0.0
        endif

        do jhor = 1, nhor
         lwcnst1(jhor) = exp(-(ztaul(jhor,jlev)/2.)/diffcoef(jhor,jlev))
         lwflag1(jhor) = ztaul(jhor,jlev)/2- &
                         diffcoef(jhor,jlev)*Log(bb(jhor)/bl(jhor))
         if(abs(lwflag1(jhor)).gt.1.E-10) then
          ED1(jhor) = ((bl(jhor)-bb(jhor)*lwcnst1(jhor))* &
                  (ztaul(jhor,jlev)/2.))/lwflag1(jhor)
         else
          ED1(jhor) = ((bl(jhor)-bb(jhor)*lwcnst1(jhor))* &
                  (ztaul(jhor,jlev)/2.))/epsilon_r
         endif 
         lwflag2(jhor) = ztaul(jhor,jlev)/2- &
                         diffcoef(jhor,jlev)*Log(bl(jhor)/bt(jhor))
         if(abs(lwflag2(jhor)).gt.1.E-10) then
          ED2(jhor) = ((bt(jhor) - bl(jhor)*lwcnst1(jhor))* &
                  (ztaul(jhor,jlev)/2.))/lwflag2(jhor)
         else
          ED2(jhor) = ((bt(jhor) - bl(jhor)*lwcnst1(jhor))* &
                 (ztaul(jhor,jlev)/2.))/epsilon_r
         endif
        enddo

        ED1(:) = ED1(:)*exp(-(1./diffcoef(:,jlev))*(ztaul(:,jlev)/2.))
        ED0(:) = ED1(:) + ED2(:)

        Dradil(:,jlev) = ED0(:) + Dradil(:,jlev-1) * &
                         exp((-1./diffcoef(:,jlev))*ztaul(:,jlev))
      enddo

      Dradil(:,nlep) = Dradil(:,nlep) + (emisfc-1.0) * Dradil(:,nlep)
      Uradil(:,nlep) = zdgscg(:) + Dradil(:,nlep) * (1.-emisfc)

      do jlev = nlep, 1, -1
 	EU0(:) = 0.0
        EU1(:) = 0.0
	EU2(:) = 0.0
        bb(:) = zdgsch(:,jlev)
	bt(:) = zdgsch(:,jlev-1)
	bl(:) = zdgsc(:,jlev)
        
        do jhor = 1, nhor
         lwcnst2(jhor) = exp(-(ztaul(jhor,jlev)/2.)/diffcoef(jhor,jlev))
         lwflag3(jhor) = ztaul(jhor,jlev)/2- &
                         diffcoef(jhor,jlev)*Log(bl(jhor)/bt(jhor))
         if(abs(lwflag3(jhor)).gt.1.E-10) then
         EU1(jhor) = ((bt(jhor) - bl(jhor)*lwcnst2(jhor))* &
                 (ztaul(jhor,jlev)/2.))/lwflag3(jhor)
         else
         EU1(jhor) = ((bt(jhor) - bl(jhor)*lwcnst2(jhor))* &
                 (ztaul(jhor,jlev)/2.))/epsilon_r
         endif
         lwflag4(jhor) = ztaul(jhor,jlev)/2- &
                         diffcoef(jhor,jlev)*Log(bb(jhor)/bl(jhor))
         if(abs(lwflag4(jhor)).gt.1.E-10) then
         EU2(jhor) = ((bl(jhor) - bb(jhor)*lwcnst2(jhor))* &
                 (ztaul(jhor,jlev)/2.))/lwflag4(jhor)
         else
         EU2(:) = ((bl(:) - bb(:)*lwcnst2(jhor))* &
                 (ztaul(:,jlev)/2.))/epsilon_r
         endif
        enddo
 
	EU2(:) = EU2(:)*exp(-(1./diffcoef(:,jlev))*(ztaul(:,jlev)/2.))
	EU0(:) = EU1(:) + EU2(:)
        Uradil(:,jlev-1) = EU0(:) + Uradil(:,jlev)* &
                           exp((-1./diffcoef(:,jlev))*ztaul(:,jlev))
      enddo
! commented by Yixiong 22/11/2012
!      ulwtoa(:) = Uradil(:,0)
      do jlev = 1, nlep
        fnetl(:,jlev) = Uradil(:,jlev) - Dradil(:,jlev)
      enddo
      do jlev = 1, nlev
	zhtrl(:,jlev) = ga/(gascon/akap) * (fnetl(:,jlev+1)-fnetl(:,jlev)) &
                       / (zdgpsigh(:,jlev+1)-zdgpsigh(:,jlev))
     !added by Salvatore
         qrad_int(:)=qrad_int(:)+(fnetl(:,jlev+1)-fnetl(:,jlev)) &
                              +  (fnets(:,jlev)-fnets(:,jlev+1))     
      enddo


!      zhtrl(:,:) = 0.0

!     ================================
!     calculate temperature tendencies
!     ================================
      do jlev = 1,nlev
        radtt(:,jlev) = (zhtrs(:,jlev) + zhtrl(:,jlev))/(ct*ww)
!        gtt(:,jlev) = gtt(:,jlev) + radtt(:,jlev)
        gtt(:,jlev) = radtt(:,jlev)
      enddo

      dgtsurf(:) = ((fnets(:,nlep) + Dradil(:,nlep))/SBC)**(0.25)
      dgtrad(:) = dgtsurf(:)
      
      else
              do jlev = 1,nlev
!               gtt(:,jlev) = gtt(:,jlev) + radtt(:,jlev)
               gtt(:,jlev) = radtt(:,jlev)
              enddo
              dgtsurf(:) = dgtrad(:)
      endif


!     regular Gaussian grid -> alternative Gaussian grid
!      call reg2alt(gtt,nlev)

!      dgtsurf(:) = ((fnets(:,nlep) + Dradil(:,nlep))/SBC)**(0.25)
      


!added by Salvatore 4/9/12
      
 
!      srad(:)=(fnets(:,nlep)-fnetl(:,nlep))/dgtsurf(:)

! commented by Yixiong 22/11/2012
!      surfsw(:) = fnets(:,nlep)                   
!      surflw(:) = SBC*dgtsurf(:)**4.-Dradil(:,nlep)


      return

      end subroutine radtrans

!     *************************************************************************
!     *************************************************************************
!     *************************************************************************

!     ==================
!     SUBROUTINE DCASTEP
!     ==================

      subroutine dcastep
      use radmod
      implicit none

!      integer itop(NHOR),ibase(NHOR),icon(NHOR)
      integer itop,ibase,icon
!      real zdtdt(NHOR,NLEV)
      real zdtdt(NLEV,NHOR)
!      real zt(NHOR,NLEV),zth(NHOR,NLEV)
      real zt(NLEV,NHOR), zth(NLEV,NHOR)
!      real ztht(NHOR)
      real ztht,zsum1,zsum2
      
      real zskap(NLEV)
      real deltsec2

      real A(5), rtr(5), rti(5)
      real thnew, delta_p, root_diff,root_diff2, zdgp(NHOR)
      
!      real qconv(NHOR,NLEV)
      real qconv(NLEV,NHOR)
      real tbefore(NHOR)    !added by Salvatore

      integer jlev,jlep,jiter,jhor,ord,ind,ICODE

      real cnst1,cnst2,prdt1(NLEV),prdt2(NLEV)
      
!added by Yixiong and Salvatore
      qconv_int(:)=0.0
      qconv_surf(:)=0.0
      sconv_surf(:)=0.0
      saconv(:)=0.0
      qconv(:,:)=0.0

      tbefore(:)= dgtsurf(:)

      ord = 4
      deltsec2 = 2.0 * SID_DAY_EARTH/ntspd
      
      zdgp(:) = exp(gp(:))     ! non-dimensional surface pressure (gp = Ln(ps))
      zdgp(:) = zdgp(:)*psmean ! dimensional surface pressure in [Pa]

!      do jlev = 1,NLEV
!       zskap(jlev)=sigma(jlev)**akap
!       zt(:,jlev)=(gt(:,jlev)+t0(jlev))*ct + gtt(:,jlev)*deltsec2*ct*ww
!       zth(:,jlev)=zt(:,jlev)/zskap(jlev)
!      enddo
 
      do jlev = 1, NLEV
         zskap(jlev) = sigma(jlev)**akap
      enddo

      do jhor = 1, NHOR
         do jlev = 1, NLEV
            zt(jlev,jhor) = (gt(jhor,jlev)+t0(jlev))*ct + &
            gtt(jhor,jlev)*deltsec2*ct*ww
            zth(jlev,jhor) = zt(jlev,jhor)/zskap(jlev)
         enddo
      enddo
      
      do jlev = 1, NLEV
         prdt1(jlev) = zskap(jlev)*dsigma(jlev)
      enddo
      
      cnst1 = gascon/(akap*ga)
      cnst2 = SBC*deltsec2

!     Exchange between the surface and the bottom layer atm.
      do jhor = 1, NHOR
        jiter=0

        ICODE=1
        if (dgtsurf(jhor) .gt. zth(nlev,jhor)) then
                ICODE =0
          delta_p = dsigma(nlev) * zdgp(jhor)
	  A(1) = -cnst1*delta_p*zt(nlev,jhor) &
                 - cnst2*dgtsurf(jhor)**4
          A(2) = cnst1* delta_p*zskap(nlev)
          A(3) = 0.0
          A(4) = 0.0
          A(5) = cnst2 
          call zrhqr(a,ord,rtr,rti)
	  root_diff =1000.0 
          do ind =1,ord
            if (rtr(ind) .gt. 0.0 .and. rti(ind) .eq. 0.0) then 
              root_diff2 = abs(rtr(ind)-dgtsurf(jhor))
              if (root_diff2.le.root_diff)then
                thnew = rtr(ind)
                root_diff = root_diff2
                ICODE = 1
              end if
            end if
          end do
          zth(nlev,jhor) = thnew
          dgtsurf(jhor) = thnew
          if (ICODE.eq.0) then
            write(*,*) 'PROBLEMS IN ZRHQR.'
          endif
        endif

 1000 continue
       icon = 0
       ibase = 1
       itop = NLEV
       ztht = 0.0
       do jlev=2,NLEM
        jlep=jlev+1
        if(zth(jlev,jhor) < zth(jlep,jhor)) then
         ibase=jlep
         itop=jlev-1
         zsum1=prdt1(jlep)+prdt1(jlev)
         zsum2=prdt1(jlep)*zth(jlep,jhor)                  &
     &           +prdt1(jlev)*zth(jlev,jhor)
         ztht=zsum2/zsum1
         icon=1
        endif
       enddo
       if(icon > 0) then
        do jlev=nlev,1,-1
          if(itop == jlev .and. zth(jlev,jhor) < ztht) then
          itop=jlev-1
          zsum1=zsum1+prdt1(jlev)
          zsum2=zsum2+prdt1(jlev)*zth(jlev,jhor)
          ztht=zsum2/zsum1
          endif
        enddo
        do jlev=1,NLEV
         if(jlev > itop .and. jlev <= ibase) then
          zth(jlev,jhor)=ztht
         endif
        enddo
        jiter=jiter+1

          if(jiter.gt.5) then
!            write(*,*) 'too many iterations'
            goto 1001
          endif
 
        goto 1000
      endif
        if(icon.eq.0 .and. dgtsurf(jhor).le.zth(nlev,jhor)) then
          goto 1001
        endif
 1001 continue

!
      do jlev=1,NLEV
       zdtdt(jlev,jhor)=(zth(jlev,jhor)*zskap(jlev)-zt(jlev,jhor))/deltsec2
!       dtdt(:,jlev)=dtdt(:,jlev)+zdtdt(:,jlev)
!added by Yixiong and Salvatore (Note that the time difference)
! 15-11-2012, Yixiong,converting array orders.
          qconv(jlev,jhor)=cnst1*dsigma(jlev)*zdgp(jhor)*zdtdt(jlev,jhor)!/deltsec2
          qconv_int(jhor)=qconv_int(jhor)+qconv(jlev,jhor)
          saconv(jhor)=saconv(jhor)+qconv(jlev,jhor)/(zth(jlev,jhor)*zskap(jlev))
!          sconv(jhor)=sconv(jhor)-qconv(jhor,jlev)/dgtsurf(jhor)       
       gtt(jhor,jlev) = gtt(jhor,jlev) + zdtdt(jlev,jhor)/(ct*ww)
      enddo

!added by Salvatore
! The convective heat flux at surface is worked out as the energy/unit time
! associated with  the temperature decrease   due to the convective adjustment.
! The assumption is that the decrement in the LW emitted by the surface is compensated
! by the convective flux
    
       qconv_surf(:)=-SBC*(tbefore(:)**4-dgtsurf(:)**4)
       sconv_surf(:)=qconv_surf(:)/dgtsurf(:)

       srad(:)=-sconv_surf(:)

!      call reg2alt(gtt,nlev)
!
!      write(nud,*) zt(:,5)
      enddo


      return
      end subroutine dcastep



!     ===============================
!     SUBROUTINE ZRHQR etc.
!     ===============================
      SUBROUTINE zrhqr(a,m,rtr,rti)  
      INTEGER m,MAXM  
      REAL a(m+1),rtr(m),rti(m)  
      CHARACTER TMP
      PARAMETER (MAXM=50)  
!CU    USES balanc,hqr  
      INTEGER j,k  
      REAL hess(MAXM,MAXM),xr,xi  
      if (m.gt.MAXM.or.a(m+1).eq.0.) then !pause 'bad args in zrhqr'  
      write (*,*) 'Bad args in zrhqr:'
      read (*,*) tmp
      end if
      do 12 k=1,m  
        hess(1,k)=-a(m+1-k)/a(m+1)  
        do 11 j=2,m  
          hess(j,k)=0.  
11      continue  
        if (k.ne.m) hess(k+1,k)=1.  
12    continue  
      call balanc(hess,m,MAXM)  
      call hqr(hess,m,MAXM,rtr,rti)  
      do 14 j=2,m  
        xr=rtr(j)  
        xi=rti(j)  
        do 13 k=j-1,1,-1  
          if(rtr(k).le.xr)goto 1  
          rtr(k+1)=rtr(k)  
          rti(k+1)=rti(k)  
13      continue  
        k=0  
1       rtr(k+1)=xr  
        rti(k+1)=xi  
14    continue  
      return  
      END   

      SUBROUTINE balanc(a,n,np)  
      INTEGER n,np  
      REAL a(np,np),RADIX,SQRDX  
      PARAMETER (RADIX=2.,SQRDX=RADIX**2)  
      INTEGER i,j,last  
      REAL c,f,g,r,s  
1     continue  
        last=1  
        do 14 i=1,n  
          c=0.  
          r=0.  
          do 11 j=1,n  
            if(j.ne.i)then  
              c=c+abs(a(j,i))  
              r=r+abs(a(i,j))  
            endif  
11        continue  
          if(c.ne.0..and.r.ne.0.)then  
            g=r/RADIX  
            f=1.  
            s=c+r  
2           if(c.lt.g)then  
              f=f*RADIX  
              c=c*SQRDX  
            goto 2  
            endif  
            g=r*RADIX  
3           if(c.gt.g)then  
              f=f/RADIX  
              c=c/SQRDX  
            goto 3  
            endif  
            if((c+r)/f.lt.0.95*s)then  
              last=0  
              g=1./f  
              do 12 j=1,n  
                a(i,j)=a(i,j)*g  
12            continue  
              do 13 j=1,n  
                a(j,i)=a(j,i)*f  
13            continue  
            endif  
          endif  
14      continue  
      if(last.eq.0)goto 1  
      return  
      END  
 
      SUBROUTINE hqr(a,n,np,wr,wi)  
      INTEGER n,np  
      REAL a(np,np),wi(np),wr(np)  
      INTEGER i,its,j,k,l,m,nn  
      REAL anorm,p,q,r,s,t,u,v,w,x,y,z  
      anorm=0.  
      do 12 i=1,n  
        do 11 j=max(i-1,1),n  
          anorm=anorm+abs(a(i,j))  
11      continue  
12    continue  
      nn=n  
      t=0.  
1     if(nn.ge.1)then  
        its=0  
2       do 13 l=nn,2,-1  
          s=abs(a(l-1,l-1))+abs(a(l,l))  
          if(s.eq.0.)s=anorm  
          if(abs(a(l,l-1))+s.eq.s)goto 3  
13      continue  
        l=1  
3       x=a(nn,nn)  
        if(l.eq.nn)then  
          wr(nn)=x+t  
          wi(nn)=0.  
          nn=nn-1  
        else  
          y=a(nn-1,nn-1)  
          w=a(nn,nn-1)*a(nn-1,nn)  
          if(l.eq.nn-1)then  
            p=0.5*(y-x)  
            q=p**2+w  
            z=sqrt(abs(q))  
            x=x+t  
            if(q.ge.0.)then  
              z=p+sign(z,p)  
              wr(nn)=x+z  
              wr(nn-1)=wr(nn)  
              if(z.ne.0.)wr(nn)=x-w/z  
              wi(nn)=0.  
              wi(nn-1)=0.  
            else  
              wr(nn)=x+p  
              wr(nn-1)=wr(nn)  
              wi(nn)=z  
              wi(nn-1)=-z  
            endif  
            nn=nn-2  
          else  
            if(its.eq.30) then !pause 'too many iterations in hqr'  
                    write(*,*) 'Too many iterations in hqr:'
                    read(*,*) tmp
            end if
            if(its.eq.10.or.its.eq.20)then  
              t=t+x  
              do 14 i=1,nn  
                a(i,i)=a(i,i)-x  
14            continue  
              s=abs(a(nn,nn-1))+abs(a(nn-1,nn-2))  
              x=0.75*s  
              y=x  
              w=-0.4375*s**2  
            endif  
            its=its+1  
            do 15 m=nn-2,l,-1  
              z=a(m,m)  
              r=x-z  
              s=y-z  
              p=(r*s-w)/a(m+1,m)+a(m,m+1)  
              q=a(m+1,m+1)-z-r-s  
              r=a(m+2,m+1)  
              s=abs(p)+abs(q)+abs(r)  
              p=p/s  
              q=q/s  
              r=r/s  
              if(m.eq.l)goto 4  
              u=abs(a(m,m-1))*(abs(q)+abs(r))  
              v=abs(p)*(abs(a(m-1,m-1))+abs(z)+abs(a(m+1,m+1)))  
              if(u+v.eq.v)goto 4  
15          continue  
4           do 16 i=m+2,nn  
              a(i,i-2)=0.  
              if (i.ne.m+2) a(i,i-3)=0.  
16          continue  
            do 19 k=m,nn-1  
              if(k.ne.m)then  
                p=a(k,k-1)  
                q=a(k+1,k-1)  
                r=0.  
                if(k.ne.nn-1)r=a(k+2,k-1)  
                x=abs(p)+abs(q)+abs(r)  
                if(x.ne.0.)then  
                  p=p/x  
                  q=q/x  
                  r=r/x  
                endif  
              endif  
              s=sign(sqrt(p**2+q**2+r**2),p)  
              if(s.ne.0.)then  
                if(k.eq.m)then  
                  if(l.ne.m)a(k,k-1)=-a(k,k-1)  
                else  
                  a(k,k-1)=-s*x  
                endif  
                p=p+s  
                x=p/s  
                y=q/s  
                z=r/s  
                q=q/p  
                r=r/p  
                do 17 j=k,nn  
                  p=a(k,j)+q*a(k+1,j)  
                  if(k.ne.nn-1)then  
                    p=p+r*a(k+2,j)  
                    a(k+2,j)=a(k+2,j)-p*z  
                  endif  
                  a(k+1,j)=a(k+1,j)-p*y  
                  a(k,j)=a(k,j)-p*x  
17              continue  
                do 18 i=l,min(nn,k+3)  
                  p=x*a(i,k)+y*a(i,k+1)  
                  if(k.ne.nn-1)then  
                    p=p+z*a(i,k+2)  
                    a(i,k+2)=a(i,k+2)-p*r  
                  endif  
                  a(i,k+1)=a(i,k+1)-p*q  
                  a(i,k)=a(i,k)-p  
18              continue  
              endif  
19          continue  
            goto 2  
          endif  
        endif  
      goto 1  
      endif  
      return  
      END  
!--------------------------end zrhqr etc.------------------------------

