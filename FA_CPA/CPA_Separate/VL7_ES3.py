from pycpa import *

# case 8 : VL7 to ES3
# ES2 -> (VL2 + VL3 + VL9) -> Switch B -> (VL6 + VL13L) -> Switch A -> (VL4 + VL8 + VL11) -> ES3


# generate an new system
s = model.System('compare')

# set up all the resouces, or vertexes
source_fromES2 = s.bind_resource(model.Resource("source_fromES4", schedulers.SPNPScheduler()))
first = s.bind_resource(model.Resource("first", schedulers.SPNPScheduler()))
switchB_to_A = s.bind_resource(model.Resource("switchB_to_A", schedulers.SPNPScheduler()))
second = s.bind_resource(model.Resource("second", schedulers.SPNPScheduler()))
switchA_to_ES3 = s.bind_resource(model.Resource("switchA_to_ES3", schedulers.SPNPScheduler()))
third = s.bind_resource(model.Resource("third", schedulers.SPNPScheduler()))

#create tasks related to the resources
t1 = source_fromES2.bind_task(model.Task("T1", wcet=14, bcet=1, scheduling_parameter=2))
t2 = first.bind_task(model.Task("(VL2 + VL3 + VL9)", wcet=159, bcet=1, scheduling_parameter=2))
t3 = switchB_to_A.bind_task(model.Task("T3", wcet=14, bcet=1, scheduling_parameter=2))
t4 = second.bind_task(model.Task("VL6 + VL13L", wcet=38, bcet=1, scheduling_parameter=2))
t5 = switchA_to_ES3.bind_task(model.Task("T5", wcet=14, bcet=1, scheduling_parameter=2))
t6 = third.bind_task(model.Task("VL4 + VL8 + VL11", wcet=165, bcet=1, scheduling_parameter=2))

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