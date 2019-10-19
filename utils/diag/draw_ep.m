

%clear;
addpath('~/bin/');

%fid='ep_00625omg_yr20.nc';
%name='rev53_r1.0_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu1.nc'
fid=strcat('data/epflux/',name)


epy=ncread(fid,'epy');
epz=ncread(fid,'epz');
lat=ncread(fid,'lat');
lev=ncread(fid,'lev');

nlat=size(lat,1);
nlev=size(lev,1);

%epyf=flipud(epy);
%latf=flipud(lat);
epyf = epy;
latf = lat;
%epz=flipud(epz);
lev=100.0*lev;

%epyf=epyf.*600.0;



div=divergence(latf,lev,-epyf',-epz');
%div=divergence(epy',epz');

scale_factor=range(latf)/range(lev);
[C,h]=contourf(latf,lev*scale_factor,div,17);
set(get(get(h,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
set(h,'LineStyle','none');
%colormap(b2r(-3E14,3E14));
%colormap('b2r');
%colormap('Gray');
maxdiv=max(max(div))
mindiv=min(min(div))
maxdiv=max(maxdiv,abs(mindiv))
disp(maxdiv)
colormap(b2r(-maxdiv,maxdiv));
hold on;
[c1,h1]=contour(latf,lev*scale_factor,div,[0 0],'k','LineWidth',2.0);
%contourf(div);
set(get(get(h1,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');
colorbar;
hold on;
epyarw=-epyf(1:2:nlat,:)'*100;
epzarw=-epz(1:2:nlat,:)';
latfarw = latf(1:2:nlat);
scale_arw=range(latfarw)/range(lev);
set(gca,'FontSize',15);

hq=quiver(latfarw,lev*scale_arw,epyarw,epzarw*scale_arw,0.5,'k','MaxHeadSize',0.2);
ylim([min(lev) max(lev)]*scale_factor);
%legend('10^3m^3');
xlabel('Latitude (degrees north)','fontsize',15);
ylabel('Pressure (hPa)','fontsize',15);
set(gca,'YTick',flipud(lev)*scale_factor);
set(gca,'YTickLabel',flipud(lev/100.0));
set(gca,'YDir','reverse');
%quiver(epy',epz','k');
hold off;

%name = '00625omg-ep-yr01-20-30';
%print(gcf,'-depsc',fname);
%saveas(gcf,fname,'eps')
name2=strrep(name, '.', '-')
saveas(gcf,strcat('pics2/epflux/',name2),'png')
