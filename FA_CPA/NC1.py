import math
import numpy as np
import matplotlib.pyplot as plt


# Define the network topology
rate_node1 = 100  # input rate of node 1 (packets per second)
rate_node2 = 100  # output rate of node 2 (packets per second)
link_capacity = 200  # capacity of the link (packets per second)

# Define the traffic characteristics
flow_size = 50  # size of the flow in packets
interarrival_time = 0.01  # interarrival time between packets (seconds)

# Calculate the arrival curve 
arrival_curve = [(rate_node1 * t, t) for t in range(flow_size)]

# Calculate the service curve
service_curve = [(min(link_capacity, rate_node2 + arrival_curve[i][0] - rate_node1) * t, t) for i, t in enumerate(range(flow_size))]

# Perform the convolution
backlog_curve = []
for i in range(flow_size):
    b_i = 0
    for j in range(i+1):
        a_j = arrival_curve[j][0]
        s_i_minus_j = service_curve[i-j][0] if i-j >= 0 else 0
        b_i = max(b_i, a_j - s_i_minus_j)
    backlog_curve.append((b_i, i))

# Calculate the delay bound
delay_bound = math.ceil(backlog_curve[-1][0] / link_capacity * 1000)  # in milliseconds

arrival_curve_mapped = [d for (d,t) in arrival_curve]
service_curve_mapped = [d for (d,t) in service_curve]
backlog_curve_mapped = [d for (d,t) in backlog_curve]

plt.plot(range(flow_size), arrival_curve_mapped, label = "arrival_curve", marker = 'x')
plt.plot(range(flow_size), service_curve_mapped, label = "service_curve", marker = 'o')
plt.plot(range(flow_size), backlog_curve_mapped, label = "backlog_curve", marker = '|')

# naming the x axis
plt.xlabel('time')
# naming the y axis
plt.ylabel('cumulative data amount')
# giving a title to my graph
plt.title('Horizontal and vertical deviation between arrival and departure cumulative curves')

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()




# print("Service Curve:", np.array(service_curve))
# print("Arrival Curve:", np.array(arrival_curve))
# print("Backlog Curve:", np.array(backlog_curve))
# print("Delay Bound:", delay_bound, "milliseconds")

# # Define the network topology
# rate_node1 = 100  # input rate of node 1 (packets per second)
# rate_node2 = 100  # output rate of node 2 (packets per second)
# link_capacity = 200  # capacity of the link (packets per second)

# # Define the traffic characteristics
# flow_size = 1000  # size of the flow in packets
# interarrival_time = 0.01  # interarrival time between packets (seconds)

# # Calculate the service curve
# service_curve = [(min(link_capacity, rate_node1 + rate_node2 - link_capacity) * t, t) for t in range(flow_size)]

# # Calculate the arrival curve
# arrival_curve = [(rate_node1 * t, t) for t in range(flow_size)]

# # Perform the convolution
# backlog_curve = []
# for i in range(len(service_curve)):
#     b_i = 0
#     for j in range(i+1):
#         s_j = service_curve[j][0]
#         a_i_minus_j = arrival_curve[i-j][1] if i-j >= 0 else 0
#         b_i = max(b_i, s_j + a_i_minus_j)
#     backlog_curve.append((b_i, i))

# # Calculate the delay bound
# delay_bound = math.ceil((flow_size - 1) / link_capacity * 1000)  # in milliseconds

# print("Service Curve:", service_curve)
# print("Arrival Curve:", arrival_curve)
# print("Backlog Curve:", backlog_curve)
# print("Delay Bound:", delay_bound, "milliseconds")
