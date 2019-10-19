clear;
fid='1omg_ut_mon_mean.nc';

t=ncread(fid,'ta',[1 1 1 1],[Inf,Inf,Inf,1]);
tm=mean(t,1);

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
		theta(j,i)=tm(1,j,i)*(1000.0/p(i)).^kappa;
	end
end






for i=1:9
        for j=1:14
                slp(j,i)=atan((tm(1,j+1,i)-tm(1,j+1,i+1))/...
                         (tm(1,j+1,i)-tm(1,j,i))) *cosphi(j);
        end
end

mslp=mean2(slp)


slp=zeros(14,9);
for i=1:9
	for j=1:14
		slp(j,i)=atan((theta(j+1,i+1)-theta(j+1,i))/...
		         (theta(j+1,i)-theta(j,i)));
        end
end

mslp=mean2(slp)



slp=zeros(14,9);
for i=1:9
        for j=1:14
                slp(j,i)=atan((theta(j+1,i+1)-theta(j+1,i))/...
                         (theta(j+1,i)-theta(j,i)))*cosphi(j);
        end
end

mslp=mean2(slp)
