#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:37:41 2023

@author: caelelmore
"""
'''Generates a mySQL querie for the ssense Database that returns information from the Database in regards to visits.
The specific attributes and values within are extracted via text file, who's name or path is the only parameter.
The file should be formatted where each line denotes a specification of what attribute you want and what value 
you want from the attribute. 

For example, "Start: 5/10/2023" would return all visits that took place after May 10, 2023.

If there are no such lines, the query generated would be a viewing of ssense.visits.

It is assumed when referring to dates that if the year is last, then month preceeds day. See example above.'''

import re
from dateutil.parser import parse

select = "SELECT v.vid, v.hid, v.rid, v.shift, v.duration, v.itime, v.otime, v.idisp, v.odisp"
from1 = " FROM visits v"
where = ""

filename = "test_pull.cfg"

with open(filename, "r") as config:
    for line in config:
        line = line.strip().split(":")
        match line[0]:
            case "shift":
                try:
                    if len(where) == 0:
                        where += " WHERE v.shift LIKE '" + line[1].replace(" ", "") + "'"
                    else:
                        where += " AND v.shift LIKE '" + line[1].replace(" ", "") +"'"
                except:
                        print('invalid format: {} is an invalid specification for attribute {}'.format(info[1:], info[0]))
                        
                        exit()
            case "hid":
                try:
                    hid_list = []
                    for a, b in re.findall(r'(\d+)-?(\d*)', str(line[1:])):
                        hid_list.extend(range(int(a), int(a)+1 if b=='' else int(b)+1))
                    if len(where) == 0:
                        where += " WHERE v.hid in ("
                    else:
                        where += " AND v.hid in ("
                    for item in hid_list:
                        where += str(item) + ","
                    where = where[:-1] + ") "
                except:
                        print('invalid format: {} is an invalid specification for attribute {}'.format(info[1:], info[0]))
                        
                        exit()
            case "uid":
                try:    
                    select += ", r.uid "
                    from1 += ", rooms r "
                    if len(where) == 0: 
                        where += " WHERE v.rid = r.rid AND r.uid in ("
                    else:
                        where += " AND v.rid = r.rid AND r.uid in (" 
                    uid_list = []
                    for a, b in re.findall(r'(\d+)-?(\d*)', str(line[1:])):
                        uid_list.extend(range(int(a), int(a)+1 if b=='' else int(b)+1))
                    for item in uid_list:
                        where += str(item) + ","
                    where = where[:-1] + ") "
                except:
                        print('invalid format: {} is an invalid specification for attribute {}'.format(info[1:], info[0]))
                        
                        exit()
            case "did":
                try:
                    select += ", h.did"
                    if "hcws h" not in from1:
                        from1 += ", hcws h "
                    if "v.hid = h.hid" not in where:
                        if len(where) == 0: 
                            where += "WHERE v.hid = h.hid AND h.did in ("
                        else:
                            where += " AND v.hid = h.hid AND h.did in ("
                    did_list = []
                    for a, b in re.findall(r'(\d+)-?(\d*)', str(line[1:])):
                        did_list.extend(range(int(a), int(a)+1 if b=='' else int(b)+1))
                    for item in did_list:
                        where += str(item) + ","
                    where = where[:-1] + ") "
                except:
                        print('invalid format: {} is an invalid specification for attribute {}'.format(info[1:], info[0]))
                        
                        exit()
            case "jtid":
                try:
                    select += ", j.jtid"
                    from1 += ", jobs j"
                    if ", hcws h" not in from1:
                        from1 += ", hcws h"
                    if len(where) == 0:
                        where += "WHERE v.hid = h.hid AND h.jid = j.jid "
                    elif "v.hid = h.hid" not in where:
                        where += " AND v.hid = h.hid AND h.jid = j.jid "
                    else:
                        where += " AND h.jid = j.jid "
                    where += " AND j.jtid in ("
                    jtid_list = []
                    for a, b in re.findall(r'(\d+)-?(\d*)', str(line[1:])):
                        jtid_list.extend(range(int(a), int(a)+1 if b=='' else int(b)+1))
                    for item in jtid_list:
                        where += str(item) + ","
                    where = where[:-1] + ") "
                except:
                        print('invalid format: {} is an invalid specification for attribute {}'.format(info[1:], info[0]))
                        
                        exit()
            case "ftid":
                try:
                    select += ", f.ftid"
                    from1 += ", facilities f"
                    if ", hcws h" not in from1:
                        from1 += ", hcws h"
                    if len(where) == 0:
                        where += "WHERE v.hid = h.hid AND h.fid = f.fid "
                    elif "v.hid = h.hid" not in where:
                        where += " AND v.hid = h.hid AND h.fid = f.fid "
                    else:
                        where += " AND h.fid = f.fid "
                    where += " AND f.ftid in ("
                    ftid_list = []
                    for a, b in re.findall(r'(\d+)-?(\d*)', str(line[1:])):
                        ftid_list.extend(range(int(a), int(a)+1 if b=='' else int(b)+1))
                    for item in ftid_list:
                        where += str(item) + ","
                    where = where[:-1] + ") "
                except:
                        print('invalid format: {} is an invalid specification for attribute {}'.format(info[1:], info[0]))
                        
                        exit()
            case "itime":
                try:
                    itime = ":".join(line[1:])
                    itime.replace("/", "-")
                    itime = parse(itime)
                    itime = str(itime.date()) + " " + str(itime.time())
                    if len(where) == 0:
                        where += "WHERE v.itime > '" + itime + "' "
                    else: 
                        where += " AND v.itime > '" + itime + "' "
                except:
                        print('invalid format: {} is an invalid specification for attribute {}'.format(info[1:], info[0]))
                        
                        exit()
            case "otime":
                try:    
                    otime = ":".join(line[1:])
                    otime.replace("/", "-")
                    otime = parse(otime)
                    otime = str(otime.date()) + " " + str(otime.time())
                    if len(where) == 0:
                        where += "WHERE v.otime < '" + otime + "' "
                    else: 
                        where += " AND v.otime < '" + otime + "' "
                except:
                        print('invalid format: {} is an invalid specification for attribute {}'.format(info[1:], info[0]))
                        
                        exit()     
            case _:
                    print("error: {} is an invalid attribute entry".format(info[0]))
                    
                    exit()        
print(select+ " " + from1 + " " + where + ";")