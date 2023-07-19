from pycpa import *

# case 1 : VL1
# ES1 -> (VL4 + VL11) -> Switch A -> (VL10) -> Switch B -> (VL12) -> ES2
# No VL12
# generate an new system
s = model.System('compare')

# set up all the resouces, or vertexes
source_fromES1 = s.bind_resource(model.Resource("ES1_switchA", schedulers.SPNPScheduler()))
first = s.bind_resource(model.Resource("VL4+VL11", schedulers.SPNPScheduler()))
switchA_to_B = s.bind_resource(model.Resource("switchA_to_B", schedulers.SPNPScheduler()))
second = s.bind_resource(model.Resource("VL10", schedulers.SPNPScheduler()))
switchB_to_ES2 = s.bind_resource(model.Resource("switchB_to_ES2", schedulers.SPNPScheduler()))
third = s.bind_resource(model.Resource("VL12", schedulers.SPNPScheduler()))

#create tasks related to the resources
t1 = source_fromES1.bind_task(model.Task("source_toES1", wcet=8, bcet=1, scheduling_parameter=2))
t2 = first.bind_task(model.Task("first", wcet=151, bcet=1, scheduling_parameter=2))
t3 = switchA_to_B.bind_task(model.Task("switchA_to_B", wcet=8, bcet=1, scheduling_parameter=2))
t4 = second.bind_task(model.Task("second", wcet=30, bcet=1, scheduling_parameter=2))
t5 = switchB_to_ES2.bind_task(model.Task("switchB_to_ES2", wcet=8, bcet=1, scheduling_parameter=2))
t6 = third.bind_task(model.Task("third", wcet=14, bcet=1, scheduling_parameter=2))

# specify precedence constraints and link all the tasks altogether:
t1.link_dependent_task(t2).link_dependent_task(t3).link_dependent_task(t4).link_dependent_task(t5).link_dependent_task(t6)

t1.in_event_model = model.PJdEventModel(P=1000, J=0)

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