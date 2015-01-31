from systemd.manager import Manager

from aj.api import *
from aj.plugins.services.api import ServiceManager, Service


@component(ServiceManager)
class SystemdServiceManager (ServiceManager):
    id = 'systemd'
    name = 'systemd'

    @classmethod
    def __verify__(cls):
        try:
            Manager()
            return True
        except:
            return False

    def __init__(self, context):
        self.systemd = Manager()

    def list(self):
        for job_name in self.systemd.get_all_jobs():
            yield self.get(job_name)

    def get(self, id):
        job = UpstartJob(id)
        service = Service(self)
        service.id = id
        service.name = self.__fix_name(id)
        try:
            service.state = job.get_status()['state']
            service.running = service.state == 'running'
        except:
            service.running = False
        return service

    def start(self, id):
        UpstartJob(id).start()

    def stop(self, id):
        UpstartJob(id).stop()

    def restart(self, id):
        UpstartJob(id).restart()
