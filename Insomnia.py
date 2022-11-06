#!/usr/bin/env python3

from Deadline.Events import *
import subprocess

def GetDeadlineEventListener():
    return Insomnia()

def CleanupDeadlineEventListener(deadlinePlugin):
    deadlinePlugin.Cleanup()

class Insomnia(DeadlineEventListener):
    def __init__(self):
        self.OnSlaveStartingJobCallback += self.OnSlaveStartingJob
        self.OnJobResumedCallback += self.OnJobStarted
        self.OnJobStartedCallback += self.OnJobStarted
        self.OnJobFinishedCallback += self.OnJobFinished
        self.OnJobFailedCallback += self.OnJobFinished
        self.OnSlaveIdleCallback += self.OnSlaveIdle

    def Cleanup(self):
        del self.OnSlaveStartingJobCallback
        del self.OnJobResumedCallback
        del self.OnJobStartedCallback
        del self.OnJobFinishedCallback
        del self.OnJobFailedCallback
        del self.OnSlaveIdleCallback

    def OnJobStarted(self, job):
        self.Start()

    def OnJobFinished(self, job):
        self.Finished()

    def OnSlaveIdle(self, slave):
        self.Finished()

    def OnSlaveStartingJob(self, job, controller):
        self.Start()

    def Start(self):
        self.LogInfo("Started")
        subprocess.call(["powercfg", "-change", "standby-timeout-ac", "0"])
        self.LogInfo("SET TO MAX SPEED")

    def Finished(self):
        time = self.GetConfigEntryWithDefault("RegularSleepTime", "20")
        subprocess.call(["powercfg", "-change", "standby-timeout-ac", time])
        self.LogInfo("SET TO BALANCED")