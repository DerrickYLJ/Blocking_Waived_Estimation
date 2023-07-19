from pycpa import *

s = model.System('Whole_model')

task_results = analysis.analyze_system(s)

# set up all the resouces
ES1 = s.bind_resource(model.Resource("ES1", schedulers.SPNPScheduler()))
ES2 = s.bind_resource(model.Resource("ES2", schedulers.SPNPScheduler()))
ES3 = s.bind_resource(model.Resource("ES3", schedulers.SPNPScheduler()))
ES4 = s.bind_resource(model.Resource("ES4", schedulers.SPNPScheduler()))
# divide the conditions happened in swtich into 3 cases
A_to_ES1 = s.bind_resource(model.Resource("Switch_A_to_ES1", schedulers.SPNPScheduler()))
A_to_ES3 = s.bind_resource(model.Resource("Switch_A_to_ES3", schedulers.SPNPScheduler()))
A_to_B = s.bind_resource(model.Resource("Switch_A_to_B", schedulers.SPNPScheduler()))
B_to_ES2 = s.bind_resource(model.Resource("Switch_B_to_ES2", schedulers.SPNPScheduler()))
B_to_ES4 = s.bind_resource(model.Resource("Switch_B_to_ES4", schedulers.SPNPScheduler()))
B_to_A = s.bind_resource(model.Resource("Switch_B_to_A", schedulers.SPNPScheduler()))

addition = s.bind_resource(model.Resource("extra resource", schedulers.SPNPScheduler()))

#create tasks related to the resources
t1 = ES1.bind_task(model.Task("VL1", wcet=8, bcet=8, scheduling_parameter=1))
t4 = ES1.bind_task(model.Task("VL4", wcet=30, bcet=30, scheduling_parameter=1))
t8 = ES1.bind_task(model.Task("VL8", wcet=14, bcet=14, scheduling_parameter=2))
t11 = ES1.bind_task(model.Task("VL11", wcet=121, bcet=121, scheduling_parameter=2))
t2 = ES2.bind_task(model.Task("VL2", wcet=8, bcet=8, scheduling_parameter=1))
t3 = ES2.bind_task(model.Task("VL3", wcet=30, bcet=30, scheduling_parameter=1))
t7 = ES2.bind_task(model.Task("VL7", wcet=14, bcet=14, scheduling_parameter=2))
t9 = ES2.bind_task(model.Task("VL9", wcet=121, bcet=121, scheduling_parameter=2))
t5 = ES3.bind_task(model.Task("VL5", wcet=8, bcet=8, scheduling_parameter=1))
t10 = ES3.bind_task(model.Task("VL10", wcet=30, bcet=30, scheduling_parameter=2))
t12 = ES3.bind_task(model.Task("VL12", wcet=14, bcet=14, scheduling_parameter=2))
t6 = ES4.bind_task(model.Task("VL6", wcet=8, bcet=8, scheduling_parameter=1))
t13 = ES4.bind_task(model.Task("VL13", wcet=30, bcet=30, scheduling_parameter=2))

t2_A_to_ES1 = A_to_ES1.bind_task(model.Task("t2_A_to_ES1", wcet=8, bcet=8, scheduling_parameter=1))
t5_A_to_ES1 = A_to_ES1.bind_task(model.Task("t5_A_to_ES1", wcet=8, bcet=8, scheduling_parameter=1))
t6_A_to_ES1 = A_to_ES1.bind_task(model.Task("t6_A_to_ES1", wcet=8, bcet=0, scheduling_parameter=1))
t7_A_to_ES1 = A_to_ES1.bind_task(model.Task("t7_A_to_ES1", wcet=14, bcet=8, scheduling_parameter=2))
t9_A_to_ES1 = A_to_ES1.bind_task(model.Task("t9_A_to_ES1", wcet=121, bcet=0, scheduling_parameter=2))
t12_A_to_ES1 = A_to_ES1.bind_task(model.Task("t12_A_to_ES1", wcet=14, bcet=8, scheduling_parameter=2))

t8_A_to_ES3 = A_to_ES3.bind_task(model.Task("t8_A_to_ES3", wcet=14, bcet=8, scheduling_parameter=2))
t4_A_to_ES3 = A_to_ES3.bind_task(model.Task("t4_A_to_ES3", wcet=30, bcet=30, scheduling_parameter=1))
t11_A_to_ES3 = A_to_ES3.bind_task(model.Task("t11_A_to_ES3", wcet=121, bcet=121, scheduling_parameter=2))
t3_A_to_ES3 = A_to_ES3.bind_task(model.Task("t3_A_to_ES3", wcet=30, bcet=30, scheduling_parameter=1))
t7_A_to_ES3 = A_to_ES3.bind_task(model.Task("t7_A_to_ES3", wcet=14, bcet=14, scheduling_parameter=2))
t9_A_to_ES3 = A_to_ES3.bind_task(model.Task("t9_A_to_ES3", wcet=121, bcet=121, scheduling_parameter=2))
t13_A_to_ES3 = A_to_ES3.bind_task(model.Task("t13_A_to_ES3", wcet=30, bcet=30, scheduling_parameter=2))

t1_A_to_B = A_to_B.bind_task(model.Task("t1_A_to_B", wcet=8, bcet=8, scheduling_parameter=1))
t8_A_to_B = A_to_B.bind_task(model.Task("t8_A_to_B", wcet=14, bcet=14, scheduling_parameter=2))
t11_A_to_B = A_to_B.bind_task(model.Task("t11_A_to_B", wcet=121, bcet=121, scheduling_parameter=2))
t10_A_to_B = A_to_B.bind_task(model.Task("t10_A_to_B", wcet=30, bcet=30, scheduling_parameter=2))
t12_A_to_B = A_to_B.bind_task(model.Task("t12_A_to_B", wcet=14, bcet=14, scheduling_parameter=2))

t1_B_to_ES2 = B_to_ES2.bind_task(model.Task("t1_B_to_ES2", wcet=8, bcet=8, scheduling_parameter=1))
t8_B_to_ES2 = B_to_ES2.bind_task(model.Task("t8_B_to_ES2", wcet=14, bcet=14, scheduling_parameter=2))
t11_B_to_ES2 = B_to_ES2.bind_task(model.Task("t11_B_to_ES2", wcet=121, bcet=121, scheduling_parameter=2))
t12_B_to_ES2 = B_to_ES2.bind_task(model.Task("t12_B_to_ES2", wcet=14, bcet=14, scheduling_parameter=2))

t11_B_to_ES4 = B_to_ES4.bind_task(model.Task("t11_B_to_ES4", wcet=121, bcet=121, scheduling_parameter=2))
t9_B_to_ES4 = B_to_ES4.bind_task(model.Task("t9_B_to_ES4", wcet=121, bcet=121, scheduling_parameter=2))
t10_B_to_ES4 = B_to_ES4.bind_task(model.Task("t10_B_to_ES4", wcet=30, bcet=30, scheduling_parameter=2))

t2_B_to_A = B_to_A.bind_task(model.Task("t2_B_to_A", wcet=8, bcet=8, scheduling_parameter=1))
t3_B_to_A = B_to_A.bind_task(model.Task("t3_B_to_A", wcet=30, bcet=30, scheduling_parameter=1))
t7_B_to_A = B_to_A.bind_task(model.Task("t7_B_to_A", wcet=14, bcet=14, scheduling_parameter=2))
t9_B_to_A = B_to_A.bind_task(model.Task("t9_B_to_A", wcet=121, bcet=121, scheduling_parameter=2))
t6_B_to_A = B_to_A.bind_task(model.Task("t6_B_to_A", wcet=8, bcet=8, scheduling_parameter=1))
t13_B_to_A = B_to_A.bind_task(model.Task("t13_B_to_A", wcet=30, bcet=30, scheduling_parameter=2))

textra = addition.bind_task(model.Task("x", wcet=8, bcet=8, scheduling_parameter=1))
#connect each virtual link with the corresponding path
t1.link_dependent_task(t1_A_to_B).link_dependent_task(t1_B_to_ES2)
t4.link_dependent_task(t4_A_to_ES3)
t8.link_dependent_task(t8_A_to_ES3)
t11.link_dependent_task(t11_A_to_ES3)
t2.link_dependent_task(t2_B_to_A).link_dependent_task(t2_A_to_ES1)
t3.link_dependent_task(t3_B_to_A).link_dependent_task(t3_A_to_ES3)
t7.link_dependent_task(t7_B_to_A).link_dependent_task(t7_A_to_ES1)
t9.link_dependent_task(t9_B_to_ES4)
t5.link_dependent_task(t5_A_to_ES1)
t10.link_dependent_task(t10_A_to_B).link_dependent_task(t10_B_to_ES4)
t12.link_dependent_task(t12_A_to_ES1)
t6.link_dependent_task(t6_B_to_A).link_dependent_task(t6_A_to_ES1)
t13.link_dependent_task(t13_B_to_A).link_dependent_task(t13_A_to_ES3)

textra.link_dependent_task(t7_A_to_ES3).link_dependent_task(t9_A_to_ES3).link_dependent_task(t12_A_to_B).link_dependent_task(t9_A_to_ES1).link_dependent_task(t11_B_to_ES4).link_dependent_task(t11_B_to_ES2).link_dependent_task(t8_A_to_B).link_dependent_task(t8_B_to_ES2).link_dependent_task(t9_B_to_A).link_dependent_task(t11_A_to_B).link_dependent_task(t12_B_to_ES2)

#set up jitter and period
t1.in_event_model = model.PJdEventModel(P=1000, J=0)
t4.in_event_model = model.PJdEventModel(P=8000, J=0)
t8.in_event_model = model.PJdEventModel(P=16000, J=0)
t11.in_event_model = model.PJdEventModel(P=32000, J=0)
t2.in_event_model = model.PJdEventModel(P=4000, J=0)
t3.in_event_model = model.PJdEventModel(P=16000, J=0)
t7.in_event_model = model.PJdEventModel(P=16000, J=0)
t9.in_event_model = model.PJdEventModel(P=64000, J=0)
t5.in_event_model = model.PJdEventModel(P=4000, J=0)
t10.in_event_model = model.PJdEventModel(P=8000, J=0)
t12.in_event_model = model.PJdEventModel(P=16000, J=0)
t6.in_event_model = model.PJdEventModel(P=2000, J=0)
t13.in_event_model = model.PJdEventModel(P=8000, J=0)
textra.in_event_model = model.PJdEventModel(P=8000, J=0)
# perform the analysis
print("\nPerforming analysis of system '%s'" % s.name)

task_results = analysis.analyze_system(s)

# print the worst case response times (WCRTs)
print("Result:")
for r in sorted(s.resources, key=str):
    for t in sorted(r.tasks & set(task_results.keys()), key=str):
        print("%s: wcrt=%d" % (t.name, task_results[t].wcrt))
        print("    b_wcrt=%s" % (task_results[t].b_wcrt_str()))

# specify paths
p1 = s.bind_path(model.Path("P1", [t1, t1_A_to_B, t1_B_to_ES2]))
p4 = s.bind_path(model.Path("P4", [t4, t4_A_to_ES3]))
p8 = s.bind_path(model.Path("P8", [t8, t8_A_to_ES3]))
p11 = s.bind_path(model.Path("p11", [t11, t11_A_to_ES3]))
p2= s.bind_path(model.Path("p2", [t2, t2_B_to_A, t2_A_to_ES1]))
p3= s.bind_path(model.Path("p3", [t3, t3_B_to_A, t3_A_to_ES3]))
p7 = s.bind_path(model.Path("p7", [t7, t7_B_to_A, t7_A_to_ES1]))
p9 = s.bind_path(model.Path("p9", [t9, t9_B_to_ES4]))
p5 = s.bind_path(model.Path("p5", [t5, t5_A_to_ES1]))
p10 = s.bind_path(model.Path("p10", [t10, t10_A_to_B, t10_B_to_ES4]))
p12 = s.bind_path(model.Path("p12", [t12, t12_A_to_ES1]))
p6 = s.bind_path(model.Path("p6", [t6, t6_B_to_A, t6_A_to_ES1]))
p13 = s.bind_path(model.Path("p13", [t13, t13_B_to_A, t13_A_to_ES3]))

paths = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]
# perform path analysis of selected paths
for p in paths:
    best_case_latency, worst_case_latency = path_analysis.end_to_end_latency(p, task_results, n=1)
    print("path %s e2e latency. best case: %d, worst case: %d" % (p.name, best_case_latency, worst_case_latency))

plot_in = [t1]
# plot input event models of selected tasks
for t in plot_in:
    plot.plot_event_model(t.in_event_model, 7, separate_plots=False, file_format='pdf', file_prefix='event-model-%s'
            % t.name, ticks_at_steps=False)