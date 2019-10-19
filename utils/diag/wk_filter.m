function [filtered_field] = wk_filter(field_raw,window_ratio)


time           = (1:1:size(field_raw,3))';
tukey_taper    = tukeywin(length(time),window_ratio);
    
    V = bsxfun(@power,time,0:1);
    M = V*pinv(V);
    
    size_raw = size(field_raw);
    filtered_scrch = M*reshape(permute(field_raw,[3 1 2]),size_raw(3),[]);
    filtered_scrch = reshape(filtered_scrch,[size_raw(3) size_raw(1) size_raw(2)]);
    filtered_scrch = permute(filtered_scrch,[2 3 1]);
    filtered_scrch = field_raw - filtered_scrch;
    
    filtered_field = filtered_scrch;
    
    for ii = 1:size(field_raw,1)
        for jj = 1:size(field_raw,2)
            filtered_field(ii,jj,:) = tukey_taper.*squeeze(filtered_scrch(ii,jj,:));
        end
    end

% older, slower
% filtered_field = zeros(size(field_raw));
%     for ii = 1:size(field_raw,1)
%         for jj = 1:size(field_raw,2)
%             P  = polyfit(time,squeeze(field_raw(ii,jj,:)),1);
%             ls_fit = polyval(P,time);
%             raw_ls = squeeze(field_raw(ii,jj,:)) - ls_fit;
%             filtered_field(ii,jj,:) = tukey_taper.*raw_ls;
%         end
%     end