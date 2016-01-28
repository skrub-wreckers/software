load('color-data/data-trunc.mat')
figure(10)
[az, el] = view;
cla;
hold on
axis equal

scatter3(green(:,1), green(:,2), green(:,3), 'g')
scatter3(  red(:,1),   red(:,2),   red(:,3), 'r')
scatter3( blue(:,1),  blue(:,2),  blue(:,3), 'b')
scatter3(black(:,1), black(:,2), black(:,3), 'k')
scatter3(white(:,1), white(:,2), white(:,3), 'w')
scatter3(yellow(:,1), yellow(:,2), yellow(:,3), 'y')
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
	{[1 -0.65 -0.65]', 16, 'r', red};
	{[-1 0.75 0.17]', 3, 'g', green};
	{[0.8 0.2 -1]', 12, 'y', yellow};
    {[-0.3 -0.9 1]', 8, 'b', blue};
	{[-1 -1 -1]', -225, 'k', black};
]';
for dir=dirs
	[dir, off, col, data] = dir{:};
	dir = dir / norm(dir);
	
	[r, g, b] = plane_surf(dir, off, 256 * sqrt(3));
	
	s = surf(r, g, b, 'FaceColor', col, 'FaceAlpha', 0.4);
	center = [128 128 128]';
	c_plane = center - dir*(dir'*center);
	
	q = quiver3(c_plane(1), c_plane(2), c_plane(3),...
		    64*dir(1), 64*dir(2), 64*dir(3),...
			'Color', col);
	q.LineWidth = 2;
	q.MaxHeadSize = 8;
	
	ok = dir'*double(data') > off;
	ok_pct = 100*mean(ok);
	
	fprintf('%c: %.2fr + %.2fg + %.2fb > %d (%.2f%%)\n', ...
		col, dir(1), dir(2), dir(3), off, ok_pct)

end

view(az, el)


