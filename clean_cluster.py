#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/21/19 4:23 PM
# @File    : clean_vm.py

# pip install python-jenkins

import jenkins, requests, json, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os, sys, time, subprocess

# Get tobe removed job list
def get_build_list(user, period):
	builds = []
	now = int(round(int(time.time()) * 1000))
	start = now - period*24*60*60*1000

	url_api = "https://mastern-jenkins-csb-openshift-qe.apps.ocp-c1.prod.psi.redhat.com/job/ocp-common/Flexy-install/api/json?pretty=true&tree=builds[id,displayName,timestamp]"
	res = requests.get(url=url_api, verify=False).json().get("builds")
	if not res:
		print ("No builds available!")
		return builds
	
	for item in res:
		if item.get("displayName") == user and item.get("timestamp") >= start:
			builds.append(item.get("id"))
			print ("Get flexy job https://mastern-jenkins-csb-openshift-qe.apps.ocp-c1.prod.psi.redhat.com/job/ocp-common/Flexy-install/" + "%s" % item.get("id"))
	return builds

def get_build_list(user):
         command = "curl -ksS https://mastern-jenkins-csb-openshift-qe.apps.ocp-c1.prod.psi.redhat.com/job/ocp-common/job/Flexy-install/ | grep display-name | grep -o '" + user + "-[0-9]\+' | awk -F- '{ print $2 }'"
         print (command)
         builds= []
         builds = os.popen(command)
         #subprocess.getoutput(command)
         #builds = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
         #process.stdout.readline()
         #if f.read(1):
         #print (builds)
         return builds

def run_jenkins_job(args,builds):
    try:
        jek = jenkins.Jenkins(args.get("server"), username=args.get("id"), password=args.get("token"))
        print ("Connected with %s." % args.get("server"))
                #builds = [6729]
        for build in builds:
            jek.build_job("ocp-common/Flexy-destroy", parameters={"BUILD_NUMBER": build}, token=args.get("token"))
            build_num = jek.get_job_info("ocp-common/Flexy-destroy")["nextBuildNumber"]-1
			#print "Remove build https://mastern-jenkins-csb-openshift-qe.apps.ocp-c1.prod.psi.redhat.com/job/ocp-common/job/Flexy-destroy/" + "%d for flexy job %s is staring." % (build_num, build)
            print ("Remove build https://mastern-jenkins-csb-openshift-qe.apps.ocp-c1.prod.psi.redhat.com/job/ocp-common/job/Flexy-destroy/" + "%d for flexy job %s is staring." % (build_num, build))
            time.sleep(5)
        return True
    except (Exception, ex):
        print ("Error:%s" % ex)
        return False

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print ("Usage: <file> userid")
        sys.exit(1)
        #full = sys.argv
        #builds = full[1:]

    args = {"server":"https://mastern-jenkins-csb-openshift-qe.apps.ocp-c1.prod.psi.redhat.com/","id":os.environ['JENKINS_USER_ID'],"token":os.environ['JENKINS_API_TOKEN']}
    #builds = get_build_list(sys.argv[1])
    builds = list(sys.argv[1:])
	#builds = get_build_list(sys.argv[1], period)
    if not builds:
        print ("No %s's job needed to be removed!!!" % sys.argv[1])
        sys.exit(1)
    if not run_jenkins_job(args, builds):
        sys.exit(1)
        if sys.argv[1] != 'zzhao':
             full = sys.argv
             builds = full[1:]
             run_jenkins_job(args, builds)
