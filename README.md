# worst_case_delay
This repo aims to solve the worst-case delay of relatively complicated network architecture with [1] Trajectory Approach; [2] Network Calculus; [3] Compositional Performance Analysis (CPA); and [4] Flow Aggregation and summarize both advantages and disadvantages of each approach and strives to seek out the optimal method under specific scenarios.

Additionally, while each approach here has advantages and shortcomings, they often provide different delay bounds with more or less pessimism, and a comprehensive comparison is still missing. More than this, when one considers a switched network (e.g., Ethernet, TSN, AFDX, NoC), how sending protocol2 and network topology 3 settings affect data/packet transmission within the web is insufficiently discussed, which leads that the worst-case delay analysis is often studied under a specified networking scenario, in other words, the formalization of worst-case delay analysis remains difficult to be generalized.

