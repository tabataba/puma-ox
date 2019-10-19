clear;
fid='gh-ob23-radonly-t.nc';

t=ncread(fid,'ta',[1 1 1 1],[Inf,Inf,Inf,1]);
%tm=mean(t,1);

p=ncread(fid,'lev');
lat=ncread(fid,'lat');
cosphi=zeros(1,30);


for i=1:30
	cosphi(i)=cos(lat(i)/180.0*pi);
end


slp=zeros(14,9); % slope (tan)
theta=zeros(15,10);
kappa=0.263;
for i=1:10
	for j=1:15
		theta(j,i)=t(1,j,i)*(1000.0/p(i)).^kappa;
	end
end
%contour(theta);
%stop;

for i=1:9
	for j=1:14
		slp(j,i)=((theta(j+1,i)-theta(j,i)))/(theta(j+1,i+1)-theta(j+1,i));
        end
end

mslp=mean2(slp)
