function [x, y, z] = plane_surf(normal, dist, size)

normal = normal / norm(normal);
center = normal * dist;

tangents = null(normal') * size;

res(1,1,:) = center + tangents * [-1;-1]; 
res(1,2,:) = center + tangents * [-1;1]; 
res(2,2,:) = center + tangents * [1;1]; 
res(2,1,:) = center + tangents * [1;-1];

x = squeeze(res(:,:,1));
y = squeeze(res(:,:,2));
z = squeeze(res(:,:,3));

end

