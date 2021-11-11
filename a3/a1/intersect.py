# add_to_node_list: just add node to the set
# add_to_edge_list just add the Line to set
# add_to_street_vex_dict:

def add_to_street_vex_dict(street_vex_dict, street_name, vex_set: set):
    if street_name not in street_vex_dict:
        street_vex_dict[street_name] = vex_set
    else:
        street_vex_dict[street_name].union(vex_set)

#
