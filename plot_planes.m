load('data-trunc.mat')
figure()
hold on
axis equal
%scatter3(green(:,3), green(:,2), green(:,1), 'g')
%scatter3(red(:,3), red(:,2), red(:,1),'r')
scatter3(blue(:,3), blue(:,2), blue(:,1), 'b')
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

g = [0 255; 0 255];
b = [0 0; 255 255];


dirs = [
	[-1 1.3 0];
	[-1 0 1.3];
	[-1 0.65 0.65];
    [-0.5 -0.65 0.65];
]';
for dir=dirs
	r1 = -(dir(2)*g + dir(3)*b) / dir(1);
	surf(r1, g, b)
	alpha(.4)
	center = [128 128 128]';
	c_plane = center - dir*(dir'*center);
	
	q = quiver3(c_plane(1), c_plane(2), c_plane(3),...
		    64*dir(1), 64*dir(2), 64*dir(3),...
			'k');
	q.LineWidth = 2;
	q.MaxHeadSize = 8;
	
	fprintf('%.2fr + %.2fg + %.2fb > 0\n', dir(1), dir(2), dir(3))

end

view(60, 45)


