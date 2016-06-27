import winrm
import pdb
import json
import sys
import time

class PyperV():
    """ 
        This class uses pywinrm to access remote winRM enabled hosts and control HyperV 2012 and 2008. 
        All commands should be available at some point to allow you to completely control HyperV from Linux!
        Commands are returned in JSON output for easy parsing.

        To enable this library to function properly you must enable Winrm on your server AND run the following
        in an administrator Powershell prompt:
        c:\> winrm set winrm/config/service/auth '@{Basic="true"}'
        c:\> winrm set winrm/config/service '@{AllowUnencrypted="true"}'
    """

    def __init__(self, user, passwd, host):
        self.hv_host = host
        self.hv_pass = passwd
        self.hv_user = user
        self.connection = winrm.Session(self.hv_host, auth=(self.hv_user, self.hv_pass))

    def run_ps_cmd(self, ps_cmd):
        r = self.connection.run_ps(ps_cmd)
        try:
            reply_out = json.loads(r.std_out) or json.loads(r.std_err)
        except ValueError:
            reply_out = r.std_out or r.std_err
        return r.status_code, reply_out

    def list_vms(self):
        pscmd = "GET-VM | ConvertTo-Json"
        ret, out = self.run_ps_cmd(pscmd)
        return out

    def get_snapshots(self, vm_name):
        pscmd = "GET-VMSNAPSHOT '%s'" % vm_name
        ret, out = self.run_ps_cmd(pscmd)
        return out

    def create_snapshot(self, vm_name, vm_snapshot):
        pscmd = "Checkpoint-VM -VMName '%s'" % vm_name

    def revert_snapshot(self, vm_name, vm_snapshot):
        pscmd = "Restore-VMSnapshot -VMName '%s' -Name '%s' -Confirm:$false" % (vm_name, vm_snapshot)
        ret, out = self.run_ps_cmd(pscmd)
        return out

    def start_vm(self, vm_name):
        pscmd = "Start-VM -Name '%s'" % vm_name
        ret, out = self.run_ps_cmd(pscmd)
        return out 
 
    def stop_vm(self, vm_name):
        pscmd = "Stop-VM -Name '%s' -TurnOff" % vm_name
        ret, out = self.run_ps_cmd(pscmd)
        return out

    def export_vm(self, vm_name, export_path, dir_name):
        full_dir = "%s%s" % (export_path, dir_name)
        # remove if exists first
        rm_dir = "Remove-Item '%s' -Force -Recurse" % full_dir
        ret, out = self.run_ps_cmd(rm_dir)
        # make a new one
        mkdir = "New-Item -ItemType Directory -Force -Path '%s'" % full_dir
        ret, out = self.run_ps_cmd(mkdir)
        # now actually export
        print "Starting export. This may take some time"
        pscmd = "Export-VM -Name '%s' -Path '%s'" % (vm_name, full_dir)
        ret, out = self.run_ps_cmd(pscmd)
        return out

if __name__ == '__main__':
    # Yea, this is real dirty.  
    hv = PyperV(user=[2], passwd=[3], host=sys.argv[4])
    if sys.argv[1] == 'revert':
        print "Reverting snapshot"
        hv.revert_snapshot(vm_name=str(sys.argv[5]), vm_snapshot=str(sys.argv[6]))
        hv.start_vm(vm_name=str(sys.argv[5]))
    if sys.argv[1] == 'export':
        start = time.time()
        print "Stopping VM"
        hv.stop_vm(vm_name=str(sys.argv[5]))
        time.sleep(5)
        print "Exporting VM" 
        hv.export_vm(vm_name=str(sys.argv[5]), export_path=str(sys.argv[6]), dir_name=str(sys.argv[7]))
        diff = time.time() - start
        print "Completed export in %s seconds!" % int(diff)

