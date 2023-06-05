#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:37:41 2023

@author: caelelmore
"""
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
                if len(where) == 0:
                    where += " WHERE v.shift = '" + line[1].replace(" ", "") + "'"
                else:
                    where += " AND v.shift = '" + line[1].replace(" ", "") +"'"
            case "hid":
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
            case "uid":
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
            case "did":
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
            case "jtid":
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
            case "ftid":
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
            case "itime":
                itime = ":".join(line[1:])
                itime.replace("/", "-")
                itime = parse(itime)
                itime = str(itime.date()) + " " + str(itime.time())
                if len(where) == 0:
                    where += "WHERE v.itime > '" + itime + "' "
                else: 
                    where += " AND v.itime > '" + itime + "' "
            case "otime":
                otime = ":".join(line[1:])
                otime.replace("/", "-")
                otime = parse(otime)
                otime = str(otime.date()) + " " + str(otime.time())
                if len(where) == 0:
                    where += "WHERE v.otime < '" + otime + "' "
                else: 
                    where += " AND v.otime < '" + otime + "' "
                
print(select+ " " + from1 + " " + where + ";")