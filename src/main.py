#!/usr/bin/env pybricks-micropython

from core.utils import get_hostname
import sandy_junior
import lilo_stitch


def main():
    hostname = get_hostname()
    if hostname in ("sandy", "junior"):
        sandy_junior.main(hostname)
    elif hostname in ("lilo", "stitch"):
        lilo_stitch.main(hostname)


if __name__ == "__main__":
    main()
