%% an attempt at a wheeler and kiladis diagram 
%% for the dry dynamical core

wavenumber_freq_sym  = zeros(Nk,Nt,num_blocks);
wavenumber_freq_asym = zeros(Nk,Nt,num_blocks);
wavenumber_freq_bg   = zeros(Nk,Nt,num_blocks);

for ii = 1:num_blocks
    ii
    sample_index = 1+(ii-1)*(block_size-overlap):ii*block_size-(ii-1)*overlap
    ft      = field(:,:,sample_index);
    
    ft      = wk_filter(ft,0.25);
    ll = length(lats)/2;
    
    ft_sym  = 0.5*(flipdim(ft(:,1:ll,:),2)+ft(:,1+ll:2*ll,:));
    ft_asym = 0.5*(-flipdim(ft(:,1:ll,:),2)+ft(:,1+ll:2*ll,:));
    
    %%fft in time and space for background, symmetric and asymmetric
    x_o_bg  = fft(ft,Nk,1)/L;
    tx_o_bg = fft(x_o_bg,Nt,3)/T;
    
    x_o_sym  = fft(ft_sym,Nk,1)/L;
    tx_o_sym = fft(x_o_sym,Nt,3)/T;
    
    x_o_asym  = fft(ft_asym,Nk,1)/L;
    tx_o_asym = fft(x_o_asym,Nt,3)/T;
    
    wavenumber_freq_bg(:,:,ii)   = 2*abs(squeeze(sum(tx_o_bg,2)));
    wavenumber_freq_sym(:,:,ii)  = 2*abs(squeeze(sum(tx_o_sym,2)));
    wavenumber_freq_asym(:,:,ii) = 2*abs(squeeze(sum(tx_o_asym,2)));
end

%%define limits of figure
end_wn        = 15;  %limit of wavenumber in figure
freq_index    = 1:Nt/2+1;
wavenum_index = [1:end_wn+1 (Nk-end_wn+1):Nk];
smooth_bg     = squeeze(mean(wavenumber_freq_sym,3));
smooth_bg     = smooth_bg + squeeze(mean(wavenumber_freq_asym,3));
smooth_bg     = flipud(fftshift(smooth_bg));
smooth_sym    = squeeze(mean(wavenumber_freq_sym,3));
smooth_sym    = flipud(fftshift(smooth_sym));
smooth_asym   = squeeze(mean(wavenumber_freq_asym,3));
smooth_asym   = flipud(fftshift(smooth_asym));
%%filtering
num_filt      = 10;
filter_121  = (1/16)*[1 2 1; 2 4 2; 1 2 1];
vec121      = 1/4*[1 2 1];

for ii=1:num_filt
    smooth_bg    = conv2(smooth_bg,filter_121,'same');
    smooth_sym   = conv2(smooth_sym,filter_121,'same');
    smooth_asym  = conv2(smooth_asym,filter_121,'same');
end

% for ii=1:size(smooth_bg,2)
%     for jj = 1:num_filt_k
%     smooth_bg(:,ii)   = conv(smooth_bg(:,ii),vec121,'same');
%     smooth_sym(:,ii)  = conv(smooth_sym(:,ii),vec121,'same');
%     smooth_asym(:,ii) = conv(smooth_asym(:,ii),vec121,'same');
%     end
% end
% 
% for kk=1:size(smooth_bg,1)
%     for ll = 1:num_filt_freq
%     smooth_bg(kk,:)   = conv(smooth_bg(kk,:),vec121,'same');
%     smooth_sym(kk,:)  = conv(smooth_sym(kk,:),vec121,'same');
%     smooth_asym(kk,:) = conv(smooth_asym(kk,:),vec121,'same');
%     end
% end

smooth_bg = ifftshift(flipud(smooth_bg));
smooth_bg = smooth_bg(wavenum_index,freq_index);
smooth_bg = flipud(fftshift(smooth_bg,1));

smooth_sym = ifftshift(flipud(smooth_sym));
smooth_sym = smooth_sym(wavenum_index,freq_index);
smooth_sym = flipud(fftshift(smooth_sym,1));

smooth_asym = ifftshift(flipud(smooth_asym));
smooth_asym = smooth_asym(wavenum_index,freq_index);
smooth_asym = flipud(fftshift(smooth_asym,1));

spec_sym      = squeeze(mean(wavenumber_freq_sym,3));
spec_sym      = spec_sym(wavenum_index,freq_index);
spec_sym      = flipud(fftshift(spec_sym,1));

spec_asym      = squeeze(mean(wavenumber_freq_asym,3));
spec_asym      = spec_asym(wavenum_index,freq_index);
spec_asym      = flipud(fftshift(spec_asym,1));

spec_bg      = squeeze(mean(wavenumber_freq_bg,3));
spec_bg      = spec_bg(wavenum_index,freq_index);
spec_bg      = flipud(fftshift(spec_bg,1));
    
% cut off topmost freq component, stay away from edge of spectral data.
freq = 0.5*linspace(0,1./timestep,Nt/2+1);
wavenum = -end_wn:1:end_wn;
freq_plot = 1:length(freq)-3;

%%plot

figure
contourf(wavenum,freq(:,freq_plot),log10(smooth_bg(:,freq_plot))',10,'linestyle','none')
colorbar
colormap(flipud(hot))
xlabel('k')
ylabel('\omega')
title('log10 background')
set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
set(gca,'ytick',0:0.05:0.5)

figure
contourf(wavenum,freq(freq_plot),log10(spec_sym(:,freq_plot))',10,'linestyle','none')
colorbar
colormap(flipud(hot))
xlabel('k')
ylabel('\omega')
title('log10 symmetric component')
set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
set(gca,'ytick',0:0.05:0.5)

figure
contourf(wavenum,freq(:,freq_plot),log10(spec_asym(:,freq_plot))',10,'linestyle','none')
colorbar
colormap(flipud(hot))
xlabel('k')
ylabel('\omega')
title('log10 asymmetric component')
set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
set(gca,'ytick',0:0.05:0.5)

figure
contourf(wavenum,freq(:,freq_plot),log10(spec_bg(:,freq_plot))',10,'linestyle','none')
colorbar
colormap(flipud(hot))
xlabel('k')
ylabel('\omega')
title('log10 background')
set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
set(gca,'ytick',0:0.05:0.5)

n = 1000; %number of points in plotting of lines

%%define matsuno SW equatorial waves
mu = cosd(mean(lat(lats)));

k_dim = linspace(-end_wn,end_wn,n)/(a*mu);
H     = [200 40 12]; %65 30 12 for 30 lev at 250mb
gwave = sqrt(g*H);
gw2   = sqrt(g*1.5e4); %%paper values are 1.3e4 for H and udop = 15
                       %%1.5e4 and 15 for 30 lev control at 250mb
                       %%1.5e5 and 25 for 30lev gpw_32
kelvin    = zeros(length(k_dim),length(H));
kelvin2   = zeros(length(k_dim),length(H));
mrg       = zeros(length(k_dim),length(H));
eig0      = zeros(length(k_dim),length(H));
mrg_eig   = zeros(length(k_dim),length(H));
eq_rossby = zeros(length(k_dim),length(H));
eq_rossby2 = zeros(length(k_dim),length(H));
eig2      = zeros(length(k_dim),length(H));
eig1      = zeros(length(k_dim),length(H));

beta = 2*om/a;
Udop = 25;   

for kk = 1:length(H)

kelvin(:,kk)     = k_dim.*gwave(kk);
kelvin2(:,kk)    = -100*k_dim+k_dim.*gwave(kk);
eq_rossby(:,kk)  = -beta*k_dim./(k_dim.^2+3*beta./gwave(kk));
eq_rossby2(:,kk)  = Udop*k_dim-beta*k_dim./(k_dim.^2+3*beta./gw2);
mrg(:,kk)  = k_dim.*gwave(kk)/2.*(1-sqrt(1+4*beta./(k_dim.^2*gwave(kk))));
eig0(:,kk) = k_dim.*gwave(kk)/2.*(1+sqrt(1+4*beta./(k_dim.^2*gwave(kk))));
eig1(:,kk) = sqrt(3*beta*gwave(kk)+k_dim.^2*gwave(kk)^2);
eig2(:,kk) = sqrt(5*beta*gwave(kk)+k_dim.^2*gwave(kk)^2);
end
kelvin    = 86400*kelvin/(2*pi);
kelvin2   = 86400*kelvin2/(2*pi);
eig0      = 86400*eig0/(2*pi);
eig1      = 86400*eig1/(2*pi);
eig2      = 86400*eig2/(2*pi);
mrg       = 86400*mrg/(2*pi);
eq_rossby = 86400*eq_rossby/(2*pi);
eq_rossby2 = 86400*eq_rossby2/(2*pi);

mrg_eig(1:n/2,:) = mrg(1:n/2,:);
mrg_eig(n/2+1:end,:) = eig0(n/2+1:end,:);
eq_rossby2(n/2+1:end,:) = 0;

figure
plot_sym = (spec_sym(:,freq_plot)'./smooth_sym(:,freq_plot)');
max_sym  = max(max(plot_sym));
% contour(wavenum,freq(freq_plot),plot_sym,1:0.25:max_sym,'k')
% hold on
contourf(wavenum,freq(freq_plot),plot_sym,linspace(1,max_sym,100),'linestyle','none')
colorbar
colormap(flipud(gray))
% title('\fontsize{12} symmetric component divided by background')
set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
% set(gca,'xtick',[-8 -5 -1 0 1 5 8])
set(gca,'ytick',[0:0.05:1]/timestep)
hold on
plot(k_dim*a,kelvin,'k','linewidth',1)
plot(k_dim*a,eq_rossby,'k','linewidth',1)
plot(k_dim*a,eq_rossby2,'k--','linewidth',1)
xlabel('\fontsize{17} wavenumber')
ylabel('\fontsize{17} frequency')
set(gca, 'FontSize', 15);
set(gcf,'PaperPositionMode','auto')
% print('-depsc','-r300',[expname '_wk2'])


figure
plot_asym = (spec_asym(:,freq_plot)'./smooth_asym(:,freq_plot)');
max_asym  = max(max(plot_asym));
% contour(wavenum,freq(freq_plot),plot_asym,1:0.25:max_asym,'k')
% hold on
contourf(wavenum,freq(freq_plot),plot_asym,linspace(1,max_asym,10),'linestyle','none')
colorbar
colormap(flipud(gray))
xlabel('\fontsize{12}k')
ylabel('\fontsize{12}\omega')
% title('asymmetric component divided by background')
set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
set(gca,'ytick',[0:0.05:0.5]/timestep)
hold on
plot(k_dim*a,mrg_eig,'k','linewidth',2)
xlabel('\fontsize{17} latitude')
ylabel('\fontsize{17} pressure')
set(gca, 'FontSize', 15);


H     = [30 75 150 1500 5000 14000] %[30 75 150]; %65 30 12 for 30 lev at 250mb
gwave = sqrt(g*H);
kelvint    = zeros(length(k_dim),length(H));
for kk = 1:length(H)
kelvint(:,kk)     = k_dim.*gwave(kk);
end
kelvint    = 86400*kelvint/(2*pi);

figure
plot_asym = (spec_bg(:,freq_plot)'./smooth_bg(:,freq_plot)');
max_asym  = max(max(plot_asym))/2;
contourf(wavenum,freq(freq_plot),plot_asym,linspace(1,max_asym,10),'linestyle','none')
colorbar
colormap(flipud(summer))
xlabel('\fontsize{12}k')
ylabel('\fontsize{12}\omega')
title('background component divided by smooth background')
set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
set(gca,'ytick',[0:0.05:0.5]/timestep)
xlabel('\fontsize{17} latitude')
hold on
plot(k_dim*a,kelvint,'k','linewidth',1)
ylabel('\fontsize{17} frequency')
set(gca, 'FontSize', 15);

ubar_dop = mean(u_zm(lats,plev));
midlat1 = ubar_dop*(k_dim-sqrt(2)*sqrt(2*om/a*mu/ubar_dop));
midlat1 = 86400*midlat1/(2*pi);
midlat2 = ubar_dop*(k_dim+sqrt(2)*sqrt(2*om/a*mu/ubar_dop));
midlat2 = 86400*midlat2/(2*pi);

% figure
% plot_sym = (spec_bg(:,freq_plot)'./smooth_bg(:,freq_plot)');
% max_sym  = max(max(plot_sym));
% % contour(wavenum,freq(freq_plot),plot_sym,1:0.25:max_sym,'k')
% % hold on
% contourf(wavenum,freq(freq_plot),plot_sym,linspace(1,max_sym,100),'linestyle','none')
% colorbar
% colormap(flipud(gray))
% set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
% % set(gca,'xtick',[-8 -5 -1 0 1 5 8])
% set(gca,'ytick',[0:0.05:0.5]/timestep)
% hold on
% plot(k_dim*a*mu,midlat1,'k','linewidth',1)
% plot(k_dim*a*mu,midlat2,'k','linewidth',1)
% % hold on
% plot(k_dim*a,kelvin(:,2),'r','linewidth',1)
% % plot(k_dim*a,eq_rossby,'k','linewidth',1)
% % plot(k_dim*a,eq_rossby2,'k--','linewidth',1)
% xlabel('\fontsize{17} wavenumber')
% ylabel('\fontsize{17} frequency')
% set(gca, 'FontSize', 15);
% % title('no symmetry/asymmetry')
% 
% figure
% plot_sym = (spec_bg(:,freq_plot)'./smooth_bg(:,freq_plot)');
% max_sym  = max(max(plot_sym));
% % contour(wavenum,freq(freq_plot),plot_sym,1:0.25:max_sym,'k')
% % hold on
% contourf(wavenum,freq(freq_plot),plot_sym,linspace(1.5,max_sym,100),'linestyle','none')
% colorbar
% colormap(flipud(gray))
% set(gca,'xtick',[-15 -10 -5 -1 0 1 5 10 15])
% % set(gca,'xtick',[-8 -5 -1 0 1 5 8])
% set(gca,'ytick',[0:0.05:0.5]/timestep)
% hold on
% plot(k_dim*a*mu,midlat1,'k','linewidth',1)
% plot(k_dim*a*mu,midlat2,'k','linewidth',1)
% % hold on
% % plot(k_dim*a,kelvin(:,2),'r','linewidth',1)
% % plot(k_dim*a,eq_rossby,'k','linewidth',1)
% % plot(k_dim*a,eq_rossby2,'k--','linewidth',1)
% xlabel('\fontsize{17} wavenumber')
% ylabel('\fontsize{17} frequency')
% set(gca, 'FontSize', 15);
% % title('no symmetry/asymmetry')

