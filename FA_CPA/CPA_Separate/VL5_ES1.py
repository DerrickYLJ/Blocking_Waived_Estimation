from pycpa import *

# case 5 : VL5
# ES3 -> (VL10L) -> Switch A -> (VL2 + VL9L + VL6) -> ES1

# generate an new system
s = model.System('compare')

# set up all the resouces, or vertexes
source_fromES3 = s.bind_resource(model.Resource("source_fromES3", schedulers.SPNPScheduler()))
first = s.bind_resource(model.Resource("first", schedulers.SPNPScheduler()))
switch_to_ES1 = s.bind_resource(model.Resource("switch_to_ES1", schedulers.SPNPScheduler()))
second = s.bind_resource(model.Resource("second", schedulers.SPNPScheduler()))

#create tasks related to the resources
t1 = source_fromES3.bind_task(model.Task("T1", wcet=8, bcet=1, scheduling_parameter=2))
t2 = first.bind_task(model.Task("VL10L", wcet=30, bcet=1, scheduling_parameter=2))
t3 = switch_to_ES1.bind_task(model.Task("T3", wcet=8, bcet=1, scheduling_parameter=2))
t4 = second.bind_task(model.Task("VL2 + VL9L + VL6L", wcet=137, bcet=1, scheduling_parameter=2))

# specify precedence constraints and link all the tasks altogether:
t1.link_dependent_task(t2).link_dependent_task(t3).link_dependent_task(t4)

t1.in_event_model = model.PJdEventModel(P=4000, J=0)

print("\nPerforming analysis of system '%s'" % s.name)
task_results = analysis.analyze_system(s)

# print the worst case response times (WCRTs)
print("Result:")
for r in sorted(s.resources, key=str):
    for t in sorted(r.tasks & set(task_results.keys()), key=str):
        print("%s: wcrt=%d" % (t.name, task_results[t].wcrt))
        print("    b_wcrt=%s" % (task_results[t].b_wcrt_str()))

# specify paths
p1 = s.bind_path(model.Path("P1", [t1, t2, t3, t4]))

paths = [p1]
# perform path analysis
for p in paths:
    best_case_latency, worst_case_latency = path_analysis.end_to_end_latency(p, task_results, n=1)
    print("path %s e2e latency. best case: %d, worst case: %d" % (p.name, best_case_latency, worst_case_latency))