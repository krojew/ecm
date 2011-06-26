# Copyright (c) 2010-2011 Robin Jarry
# 
# This file is part of EVE Corporation Management.
# 
# EVE Corporation Management is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or (at your 
# option) any later version.
# 
# EVE Corporation Management is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
# more details.
# 
# You should have received a copy of the GNU General Public License along with 
# EVE Corporation Management. If not, see <http://www.gnu.org/licenses/>.

__date__ = "2011-03-09"
__author__ = "diabeteman"




from threading import Thread
from datetime import datetime, timedelta

import logging
logger = logging.getLogger(__name__)



class TaskThread(Thread):
    
    def __init__(self, tasks):
        super(self.__class__, self).__init__()
        self.tasks = tasks
        
    def run(self):
        logger.debug("executing %d task(s)" % len(self.tasks))
        for task in self.tasks:
            try:
                if task.is_running:
                    continue
                else:
                    task.is_running = True
                    task.save()
                logger.info(unicode(task) + " triggered")
                task.run()
                logger.info(unicode(task) + " success")
                task.is_last_exec_success = True
            except:
                task.is_last_exec_success = False
            finally:
                if task.is_one_shot and task.is_last_exec_success:
                    logger.info(unicode(task) + " was one shot, deleting...")
                    task.delete()
                else:
                    delta = task.frequency * task.frequency_units
                    task.next_execution = datetime.now() + timedelta(seconds=delta)
                    task.is_running = False
                    task.save()