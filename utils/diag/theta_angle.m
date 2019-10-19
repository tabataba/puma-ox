t = [1.5814,0.7761,0.3262,0.1813,0.1749,0.1746,0.1653,0.1519];
semilogy(1.6376./t,'sb--','MarkerSize',10,'markerfacecolor','b');
set(gca,'XTick',[1:8]);
set(gca,'ylim',[0.5 15])
set(gca,'XTickLabel',{'8';'4';'2';'1';'1/2';'1/4';'1/8';'1/16'});
set(gca,'fontsize',15);
xlabel('\Omega/{\Omega_e}');
ylabel('Scaled isentropic slope')
hold on;
t1 = [0.5,0.2506,0.2365,0.1372,0.1127,0.1101,0.0914,0.0774];
plot(0.7./t1,'or--','MarkerSize',10,'markerfacecolor','r');
t5 = [0.1314,0.0805,0.0786,0.0750,0.0620,0.0529,0.0510,0.0363];
plot(0.2850./t5,'^k--','Markersize',10,'markerfacecolor','k');

legend('Greenhouse','Neutral-greenhouse','Anti-greenhouse','location','southeast');
h=findobj(gcf,'type','axes','tag','legend');
pos = get(h,'position');
pos(1) =0.8*pos(1);
pos(3) =1.6*pos(3);
set(h,'position',pos);


fname = 'pumag-theta-slp-scaled';
print(gcf,'-depsc',fname);
