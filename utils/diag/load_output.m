
file='/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/noseasons_pumagt_arcb/rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu0/'
%file='/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pumagt_arcb_parameters_backup/rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu1/'

ncfile=strcat(file,'PUMAG_NWPD12_M.001.nc')
ncfile1=strcat(file,'PUMAG_NWPD12_M.002.nc')
ncfile2=strcat(file,'PUMAG_NWPD12_M.003.nc')
ncfile3=strcat(file,'PUMAG_NWPD12_M.004.nc')
ncfile4=strcat(file,'PUMAG_NWPD12_M.005.nc')
ncfile5=strcat(file,'PUMAG_NWPD12_M.006.nc')
ncfile6=strcat(file,'PUMAG_NWPD12_M.007.nc')
ncfile7=strcat(file,'PUMAG_NWPD12_M.008.nc')
ncfile8=strcat(file,'PUMAG_NWPD12_M.009.nc')
ncfile9=strcat(file,'PUMAG_NWPD12_M.010.nc')
ncfile10=strcat(file,'PUMAG_NWPD12_M.011.nc')
ncfile11=strcat(file,'PUMAG_NWPD12_M.012.nc')
%load netcdf model output
ncid = netcdf.open(ncfile,'nowrite');

%pick out times for making figures
st = 2*365+1;en = 10*365;
st=4*360+1; en=360*5%*5
t_plot   = st:en;

%constants
a=6.371e6; g = 9.80; om = 7.292e-5; p_00 = 1000;

expname  = 'con' 
plev = 6; %pressure level for analysis

%%dimensions
p_level=ncread(ncfile,'lev');
lat=ncread(ncfile,'lat');
lon=ncread(ncfile,'lon');
timefull=ncread(ncfile,'time');
timefull1=ncread(ncfile1,'time');
timefull2=ncread(ncfile2,'time');
timefull3=ncread(ncfile3,'time');
timefull4=ncread(ncfile4,'time');
timefull5=ncread(ncfile5,'time');
timefull6=ncread(ncfile6,'time');
timefull7=ncread(ncfile7,'time');
timefull8=ncread(ncfile8,'time');
timefull9=ncread(ncfile9,'time');
timefull10=ncread(ncfile10,'time');
timefull11=ncread(ncfile11,'time');

p_l=size(p_level,1)
lat_l=size(lat,1)
lon_l=size(lon,1)

hgt=ncread(ncfile,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt1=ncread(ncfile1,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt2=ncread(ncfile2,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt3=ncread(ncfile3,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt4=ncread(ncfile4,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt5=ncread(ncfile5,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt6=ncread(ncfile6,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt7=ncread(ncfile7,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt8=ncread(ncfile8,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt9=ncread(ncfile9,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt10=ncread(ncfile10,'zg',[1 1 1 1],[Inf Inf Inf Inf]);
hgt11=ncread(ncfile11,'zg',[1 1 1 1],[Inf Inf Inf Inf]);

hgt=(cat(4,hgt,hgt1,hgt2,hgt3,hgt4,hgt5,hgt6,hgt7,hgt8,hgt9,hgt10,hgt11));
timefull=(cat(1,timefull,timefull1,timefull2,timefull3,timefull4,timefull5,timefull6,timefull7,timefull8,timefull9,timefull10,timefull11));

%hgt=hgt1;
%timefull=timefull1;

time_l=size(timefull,1)
size(hgt)

%[lon lon_l]       = ncload(ncid,'lon',0,0,0)
%[lat lat_l]       = ncload(ncid,'lat',0,0,0)
%[p_level p_l]     = ncload(ncid,'lev',0,0,0)
%?%[p_half ~]        = ncload(ncid,'levh',0,0,0)
%?%[timefull time_l] = ncload(ncid,'time',0,0,0)

time              = timefull(t_plot)
timestep          = mean(diff(time))
dims              = [lon_l lat_l p_l time_l en-st+1]
%stop
%%fields
%[hfull hgt]    = ncload(ncid,'zg',t_plot,dims,0);

%%wheeler-kiladis diagram

lats         = 27:38;%pick out latitudes between +/-15 degrees
block_size   = 128%30*12%90*12%90*12%128; %assuming once daily output, 128 day blocks is standard from WK method. if outputting more than once/day to look at higher frequency phenomena, divide this 128 by timestep, where timestep = 1/(number of model outputs per day)
overlap      = 78%18*12%55*12%78*12; %from WK. also divide by timestep
num_blocks   = floor((en-st)/(block_size-overlap))-2

field = hgt; %geopotential height as field to be analyzed
field = squeeze(field(:, lats, plev, :));   

Nk = 2.^nextpow2(size(field, 1));              
Nt = 2.^nextpow2(block_size);               
L = size(field, 1);                      
T = block_size;  

wheeler_kiladis %runs the wheeler_kiladis.m script
