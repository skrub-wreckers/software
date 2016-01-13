load('data-trunc.mat')
figure(10)
[az, el] = view;
cla;
hold on
axis equal

scatter3(green(:,3), green(:,2), green(:,1), 'g')
scatter3(  red(:,3),   red(:,2),   red(:,1), 'r')
scatter3( blue(:,3),  blue(:,2),  blue(:,1), 'b')
scatter3(black(:,3), black(:,2), black(:,1), 'k')
scatter3(white(:,3), white(:,2), white(:,1), 'w')
xlim([0 255])
ylim([0 255])
zlim([0 255])
xlabel('R')
ylabel('G')
zlabel('B')
grid on

ax = gca;
ax.XTick = 0:64:256;
ax.YTick = 0:64:256;
ax.ZTick = 0:64:256;

dirs = [
	{[1 -0.65 -0.65]', 0, 'r'};
	{[-0.9 1 -0.3]', 0, 'g'};
    {[-0.4 -1 1]', 0, 'b'};
]';
for dir=dirs
	[dir, off, col] = dir{:};
	dir = dir / norm(dir);
	
	[r, g, b] = plane_surf(dir, off, 256 * sqrt(3))
	
	s = surf(r, g, b, 'FaceColor', col, 'FaceAlpha', 0.4);
	center = [128 128 128]';
	c_plane = center - dir*(dir'*center);
	
	q = quiver3(c_plane(1), c_plane(2), c_plane(3),...
		    64*dir(1), 64*dir(2), 64*dir(3),...
			'Color', col);
	q.LineWidth = 2;
	q.MaxHeadSize = 8;
	
	fprintf('%.2fr + %.2fg + %.2fb > 0\n', dir(1), dir(2), dir(3))

end

view(az, el)


