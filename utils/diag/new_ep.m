% --------------------------------------------------------------
% This routine calculates the latitudinal(\phi) and vertical(p)
% components of the full Eliassen-Palm flux in spherical geometry
% 
% Based on the expression of E-P flux in C.Lee's thesis(eq (3.21))
% --------------------------------------------------------------


%clear;
% Read variables from netcdf file
% fid='1omg_t127_uvwpt.nc';
%name='rev53_r1.0_res64_radius1.00_taufr1.0_psurf5.0_pref5.0_taus0.00_tausurf360_nmu0'

fid=strcat(strcat('pumagt_arcb_parameters/',name),'/PUMAG.010.nc');

%fid='00625omg_uvwpt_mon_mean.nc';

u=ncread(fid,'ua',[1 1 1 1],[Inf Inf Inf Inf]);
v=ncread(fid,'va',[1 1 1 1],[Inf Inf Inf Inf]);
w=ncread(fid,'wap',[1 1 1 1],[Inf Inf Inf Inf]);
t=ncread(fid,'ta',[1 1 1 1],[Inf Inf Inf Inf]);

% zonal mean u
um=mean(u,1);
vm=mean(v,1);
wm=mean(w,1);

p=ncread(fid,'lev');
lat=ncread(fid,'lat');
lon=ncread(fid,'lon');
time=ncread(fid,'time');

nlev=size(p,1)
nlat=size(lat,1)
nlon=size(lon,1)
ntime=size(time,1)
size(u)
size(um)

cosphi=zeros(1,nlat);
cosphi(:)=cos(lat(:)*pi/180.0);

tr=mean(t,1); % zonal mean temperature
%tr=mean(tzm,2); % reference temperature, averaged further on lat


%------------------stability factor d theta/d p-----------------------
kappa=0.286;
thetar=zeros(nlat,nlev,ntime);
dthdp=zeros(nlat,nlev,ntime);
% Convert T_r to theta_r
for k=1:ntime
for i=1:nlev
    for j=1:nlat
        thetar(j,i,k)=tr(1,j,i,k)*(1000/p(i)).^kappa;
    end
end
end

% the stability parameter, d thetar/d p
for k=1:ntime
dthdp(:,1,k)=(thetar(:,2,k)-thetar(:,1,k))/((p(2)-p(1))*100);
for i=2:9
    dthdp(:,i,k)=(thetar(:,i+1,k)-thetar(:,i-1,k))/((p(i+1)-p(i-1))*100);
end
dthdp(:,10,k)=(thetar(:,10,k)-thetar(:,9,k))/((p(10)-p(9))*100);
end

s = 1
%--------------------- d um/d p ------------------------------------
dumdp=zeros(nlat,nlev,ntime);
for k=1:ntime
dumdp(:,1,k)=(um(1,:,2,k)-um(1,:,1,k))/((p(2)-p(1))*100);
for i=2:9
   dumdp(:,i,k)=(um(1,:,i+1,k)-um(1,:,i-1,k))/((p(i+1)-p(i-1))*100);
end
dumdp(:,10,k)=(um(1,:,10,k)-um(1,:,9,k))/((p(10)-p(9))*100);
end

%---------------------d um*cos(phi)/d phi ---------------------------
dudphi=zeros(nlat,nlev,ntime);
for k=1:ntime
dudphi(1,:,k)=(um(1,2,:,k)*cosphi(2)-um(1,1,:,k)*cosphi(1))/...
            ((lat(2)-lat(1))*pi/180.0);
for j=2:nlat-1
    dudphi(j,:,k)= (um(1,j+1,:,k)*cosphi(j+1)-um(1,j-1,:,k)*cosphi(j-1))/...
        ((lat(j+1)-lat(j-1))*pi/180.0);
end
dudphi(nlat,:,k)=(um(1,nlat,:,k)*cosphi(nlat)-um(1,nlat-1,:,k)*cosphi(nlat-1))/...
             ((lat(nlat)-lat(nlat-1))*pi/180.0);
end
s = 2
    
%-----------------Coriolis parameter f-----------------------------
omega=7.292E-5;
f=zeros(1,nlat);
f(:)=2*omega*sin(lat(:)/180.0*pi);
a=6400000.0;  % Earth radius
g=9.8;

%----------------- u'v'-----------------------------------------
%		theta(:,:,i,k)=t(:,:,i,k)*(1000.0/p(i)).^kappa;
for i = 1:nlev
	theta(:,:,i,:) = t(:,:,i,:)*(1000.0/p(i)).^kappa;
end

		for l = 1:nlat
			ua(l,:,:,:) = u(l,:,:,:)-um(1,:,:,:);
			va(l,:,:,:) = v(l,:,:,:)-vm(1,:,:,:);
%			ta(:,j,i,k) = theta(:,j,i,k)-thm(1,j,i,k);
			tha(l,:,:,:) = theta(l,:,:,:)-reshape(thetar(:,:,:),1,nlat,nlev,ntime);
			wa(l,:,:,:) = w(l,:,:,:)-wm(1,:,:,:);
			cuv(l,:,:,:) = ua(l,:,:,:).*va(l,:,:,:);
			cvt(l,:,:,:) = va(l,:,:,:).*tha(l,:,:,:);
			cuw(l,:,:,:) = ua(l,:,:,:).*wa(l,:,:,:);
		end
		mcuv=mean(cuv,1);
		mcvt=mean(cvt,1);
		mcuw=mean(cuw,1);



s = 3
%-------------------epy component---------------------------------
epy=zeros(nlat,nlev,ntime);
epyt=zeros(nlat,nlev,ntime);
theta=zeros(nlon,nlat,nlev,ntime);
for k=1:ntime
for i=1:nlev
    theta(:,:,i,k)=t(:,:,i,k)*(1000/p(i)).^kappa;
    for j=1:nlat
%        cm=-cov(u(:,j,i,k),v(:,j,i,k)); % covariance matrix
%        cmt=cov(v(:,j,i,k),theta(:,j,i,k));
%        epyt(j,i,k)=cm(1,2)-dumdp(j,i,k)*cmt(1,2)/dthdp(j,i,k);
        epyt(j,i,k)=mcuv(1,j,i,k)-dumdp(j,i,k)*mcvt(1,j,i,k)/dthdp(j,i,k);
        epy(j,i,k)=2*pi*a^2*(cosphi(j).^2)/g*epyt(j,i,k);
        epy(j,i) = a*cosphi(j)*epyt(j,i);
    end
end
end

%-------------------epz component----------------------------------
epz=zeros(nlat,nlev,ntime);
%epztest=zeros(30,10);
for k=1:ntime
for i=1:nlev
%    theta(:,:,i)=t(:,:,i)*(1000/p(i)).^kappa;
    for j=1:nlat
%        cmt=cov(v(:,j,i,k),theta(:,j,i,k));
%        cmw=-cov(u(:,j,i,k),w(:,j,i,k));
%        epz(j,i,k)=cmw(1,2)-...
%            (dudphi(j,i,k)/(a*cosphi(j))-f(j))*cmt(1,2)/dthdp(j,i,k);
        epz(j,i,k)=mcuw(1,j,i,k)+...
            (dudphi(j,i,k)/(a*cosphi(j))-f(j))*mcvt(1,j,i,k)/dthdp(j,i,k);
 
        epz(j,i,k)=2*pi*a^3*cosphi(j)^2/g*epz(j,i,k);
%        epz(j,i) = a*cosphi(j)*epz(j,i);
    end
end
end

epy=mean(epy,3);
epz=mean(epz,3);

%epy=epy*10.0;

%---------------------netcdf output-------------------------------
fido=strcat(strcat('data/epflux/',name),'.nc');

nccreate(fido,'lat','Dimensions',{'lat',nlat});
nccreate(fido,'lev','Dimensions',{'lev',nlev});
nccreate(fido,'epy','Dimensions',{'lat' nlat 'lev' nlev});
nccreate(fido,'epz','Dimensions',{'lat' nlat 'lev' nlev});

ncwrite(fido,'lat',lat);
ncwrite(fido,'lev',p);
ncwrite(fido,'epy',epy);
ncwrite(fido,'epz',epz);
