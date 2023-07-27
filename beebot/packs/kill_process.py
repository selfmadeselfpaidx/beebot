from pydantic import BaseModel, Field

from beebot.packs.system_base_pack import SystemBasePack

PACK_NAME = "kill_process"
PACK_DESCRIPTION = "Terminates the process with the given PID and returns its output"


class KillProcessArgs(BaseModel):
    pid: str = Field(..., description="The PID")


class KillProcess(SystemBasePack):
    name = PACK_NAME
    description = PACK_DESCRIPTION
    args_schema = KillProcessArgs
    categories = ["Multiprocess"]

    def _run(self, pid: str) -> dict[str, str]:
        # TODO: Support for daemonized processes from previous runs
        process = self.body.processes.get(int(pid))
        if not process:
            return "Error: Process does not exist."

        status = process.poll()
        if status is None:
            process.kill()

        return (
            f"The process has been killed. Output: {process.stdout}. {process.stderr}"
        )
