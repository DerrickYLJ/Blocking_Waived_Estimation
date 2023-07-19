from pycpa import *

# case 19 : VL12 to ES2
# VL10 -> VL5 -> VL12 -> switch_A (VL1) to Switch B -> VL1 -> VL8 -> VL11 -> VL9 ->switch B (VL1) to ES4 
# ES3 -> (VL5 + VL10) -> Switch A -> (VL1 + VL8 + VL11) -> Switch B -> (None) -> ES4

# generate an new system
s = model.System('compare')

# set up all the resouces, or vertexes
source_fromES3 = s.bind_resource(model.Resource("source_fromES3", schedulers.SPNPScheduler()))
first = s.bind_resource(model.Resource("first", schedulers.SPNPScheduler()))
switchA_to_B = s.bind_resource(model.Resource("switchA_to_B", schedulers.SPNPScheduler()))
second = s.bind_resource(model.Resource("second", schedulers.SPNPScheduler()))
switchB_to_ES4 = s.bind_resource(model.Resource("switchB_to_ES4", schedulers.SPNPScheduler()))
third = s.bind_resource(model.Resource("third", schedulers.SPNPScheduler()))

#create tasks related to the resources
t1 = source_fromES3.bind_task(model.Task("T1", wcet=14, bcet=1, scheduling_parameter=2))
t2 = first.bind_task(model.Task("VL5 + VL10", wcet=38, bcet=1, scheduling_parameter=2))
t3 = switchA_to_B.bind_task(model.Task("T3", wcet=14, bcet=1, scheduling_parameter=2))
t4 = second.bind_task(model.Task("VL1 + VL8 + VL11", wcet=143, bcet=1, scheduling_parameter=2))
t5 = switchB_to_ES4.bind_task(model.Task("T5", wcet=14, bcet=1, scheduling_parameter=2))
t6 = third.bind_task(model.Task("None", wcet=0, bcet=0, scheduling_parameter=2))

# specify precedence constraints and link all the tasks altogether:
t1.link_dependent_task(t2).link_dependent_task(t3).link_dependent_task(t4).link_dependent_task(t5).link_dependent_task(t6)

t1.in_event_model = model.PJdEventModel(P=16000, J=0)

print("\nPerforming analysis of system '%s'" % s.name)
task_results = analysis.analyze_system(s)

# print the worst case response times (WCRTs)
print("Result:")
for r in sorted(s.resources, key=str):
    for t in sorted(r.tasks & set(task_results.keys()), key=str):
        print("%s: wcrt=%d" % (t.name, task_results[t].wcrt))
        print("    b_wcrt=%s" % (task_results[t].b_wcrt_str()))

# specify paths
p1 = s.bind_path(model.Path("P1", [t1, t2, t3, t4, t5, t6]))

paths = [p1]
# perform path analysis
for p in paths:
    best_case_latency, worst_case_latency = path_analysis.end_to_end_latency(p, task_results, n=1)
    print("path %s e2e latency. best case: %d, worst case: %d" % (p.name, best_case_latency, worst_case_latency))