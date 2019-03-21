import rosbag
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x =[]
y =[]
z =[]
xd=[]
yd=[]
zd=[]
xs=[]
ys=[]
zs=[]
xds=[]
yds=[]
zds=[]
clock =[]
clock2 =[]
clock3 =[]
clock4 =[]
bag = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/2019.1.30/test.bag')
bag2 = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/2019.1.30/test2.bag')
bag3 = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/2019.1.30/test3.bag')
bag4 = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/2019.1.30/test4.bag')
for topic, msg, t in bag.read_messages(topics=['/mavros/local_position/pose']):
    x.append(msg.pose.position.x)
    y.append(msg.pose.position.y)
    z.append(msg.pose.position.z)
    clock.append(t.to_sec())

for topic, msg, t in bag2.read_messages(topics=['/mavros/local_position/velocity']):
    xd.append(msg.twist.linear.x)
    yd.append(msg.twist.linear.y)
    zd.append(msg.twist.linear.z)
    clock2.append(t.to_sec())

for topic, msg, t in bag3.read_messages(topics=['/mavros/setpoint_position/local']):
    xs.append(msg.pose.position.x)
    ys.append(msg.pose.position.y)
    zs.append(msg.pose.position.z)
    clock3.append(t.to_sec())

for topic, msg, t in bag4.read_messages(topics=['/mavros/setpoint_velocity/cmd_vel']):
    xds.append(msg.linear.x)
    yds.append(msg.linear.y)
    zds.append(msg.linear.z)
    clock4.append(t.to_sec())


bag.close()
bag2.close()
bag3.close()
bag4.close()
x = np.array(x)
y = np.array(y)
z = np.array(z)
xd = np.array(xd)
yd = np.array(yd)
zd = np.array(zd)
xs = np.array(xs)
ys = np.array(ys)
zs = np.array(zs)
xds = np.array(xds)
yds = np.array(yds)
zds = np.array(zds)
clock = np.array(clock)
clock2 = np.array(clock2)
clock3 = np.array(clock3)
clock4 = np.array(clock4)
clock2 =clock2-clock[1]
clock3 =clock3-clock[1]
clock4 =clock4-clock[1]
clock =clock-clock[1]

#print xs.shape
print xd
#print clock
plt.figure(1)
plt.subplot(321)
plt.plot(clock,x)
plt.plot(clock3,xs)
plt.title("x")

plt.subplot(322)
plt.plot(clock2,xd)
plt.title("xd")
plt.plot(clock4,xds)

plt.subplot(323)
plt.plot(clock,y)
plt.plot(clock3,ys)
plt.title("y")

plt.subplot(324)
plt.plot(clock2,yd)
plt.plot(clock4,yds)
plt.title("yd")

plt.subplot(325)
plt.plot(clock,z)
plt.plot(clock3,zs)
plt.title("z")

plt.subplot(326)
plt.plot(clock2,zd)
plt.plot(clock4,zds)
plt.title("zd")

fig=plt.figure(2)
ax2 = Axes3D(fig)
ax2.plot(x,y,z)
ax2.plot(xs,ys,zs)
ax2.set_zlim(0, 3)
plt.show()


