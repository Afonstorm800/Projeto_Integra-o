"""
Job and Process Control Module
Defines a complete project workflow with job orchestration
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime
from enum import Enum


class JobStatus(Enum):
    """Status of a job"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class Job:
    """Represents a single job in a workflow"""
    
    def __init__(self, name: str, func: Callable, 
                 depends_on: Optional[List[str]] = None,
                 params: Optional[Dict[str, Any]] = None):
        """
        Initialize a job
        
        Args:
            name: Job name
            func: Function to execute
            depends_on: List of job names this job depends on
            params: Parameters to pass to the function
        """
        self.name = name
        self.func = func
        self.depends_on = depends_on or []
        self.params = params or {}
        self.status = JobStatus.PENDING
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None
    
    def execute(self, context: Dict[str, Any]) -> Any:
        """
        Execute the job
        
        Args:
            context: Execution context with shared data
            
        Returns:
            Job result
        """
        self.status = JobStatus.RUNNING
        self.start_time = datetime.now()
        
        try:
            # Merge context and params
            execution_params = {**self.params, 'context': context}
            self.result = self.func(**execution_params)
            self.status = JobStatus.SUCCESS
            return self.result
        except Exception as e:
            self.status = JobStatus.FAILED
            self.error = str(e)
            raise
        finally:
            self.end_time = datetime.now()
    
    def get_duration(self) -> Optional[float]:
        """Get job execution duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None


class Pipeline:
    """Orchestrates a series of jobs in a workflow"""
    
    def __init__(self, name: str):
        """
        Initialize a pipeline
        
        Args:
            name: Pipeline name
        """
        self.name = name
        self.jobs: Dict[str, Job] = {}
        self.context: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"Pipeline.{name}")
    
    def add_job(self, job: Job) -> None:
        """
        Add a job to the pipeline
        
        Args:
            job: Job to add
        """
        if job.name in self.jobs:
            raise ValueError(f"Job '{job.name}' already exists in pipeline")
        self.jobs[job.name] = job
    
    def remove_job(self, job_name: str) -> None:
        """
        Remove a job from the pipeline
        
        Args:
            job_name: Name of job to remove
        """
        if job_name in self.jobs:
            del self.jobs[job_name]
    
    def get_execution_order(self) -> List[str]:
        """
        Calculate execution order based on dependencies
        
        Returns:
            Ordered list of job names
        """
        ordered = []
        visited = set()
        
        def visit(job_name: str):
            if job_name in visited:
                return
            if job_name not in self.jobs:
                raise ValueError(f"Job '{job_name}' not found in pipeline")
            
            job = self.jobs[job_name]
            for dep in job.depends_on:
                visit(dep)
            
            visited.add(job_name)
            ordered.append(job_name)
        
        for job_name in self.jobs:
            visit(job_name)
        
        return ordered
    
    def run(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute all jobs in the pipeline
        
        Args:
            initial_context: Initial context data
            
        Returns:
            Final context with results
        """
        if initial_context:
            self.context.update(initial_context)
        
        execution_order = self.get_execution_order()
        self.logger.info(f"Starting pipeline '{self.name}' with {len(execution_order)} jobs")
        
        for job_name in execution_order:
            job = self.jobs[job_name]
            self.logger.info(f"Executing job '{job_name}'")
            
            # Check dependencies
            can_run = True
            for dep_name in job.depends_on:
                dep_job = self.jobs[dep_name]
                if dep_job.status != JobStatus.SUCCESS:
                    self.logger.warning(
                        f"Skipping job '{job_name}' due to failed dependency '{dep_name}'"
                    )
                    job.status = JobStatus.SKIPPED
                    can_run = False
                    break
            
            if not can_run:
                continue
            
            try:
                result = job.execute(self.context)
                self.context[f'job_{job_name}_result'] = result
                duration = job.get_duration()
                self.logger.info(
                    f"Job '{job_name}' completed successfully in {duration:.2f}s"
                )
            except Exception as e:
                self.logger.error(f"Job '{job_name}' failed: {str(e)}")
                raise
        
        self.logger.info(f"Pipeline '{self.name}' completed")
        return self.context
    
    def get_status_summary(self) -> Dict[str, Any]:
        """
        Get summary of pipeline status
        
        Returns:
            Status summary
        """
        statuses = {status: 0 for status in JobStatus}
        total_duration = 0
        
        for job in self.jobs.values():
            statuses[job.status] += 1
            duration = job.get_duration()
            if duration:
                total_duration += duration
        
        return {
            'pipeline': self.name,
            'total_jobs': len(self.jobs),
            'status_counts': {status.value: count for status, count in statuses.items()},
            'total_duration': total_duration,
            'jobs': {
                name: {
                    'status': job.status.value,
                    'duration': job.get_duration(),
                    'error': job.error
                }
                for name, job in self.jobs.items()
            }
        }


class ProcessController:
    """Manages multiple pipelines and provides advanced control"""
    
    def __init__(self):
        self.pipelines: Dict[str, Pipeline] = {}
        self.logger = logging.getLogger("ProcessController")
    
    def add_pipeline(self, pipeline: Pipeline) -> None:
        """Add a pipeline to the controller"""
        self.pipelines[pipeline.name] = pipeline
    
    def get_pipeline(self, name: str) -> Optional[Pipeline]:
        """Get a pipeline by name"""
        return self.pipelines.get(name)
    
    def run_pipeline(self, name: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run a specific pipeline"""
        if name not in self.pipelines:
            raise ValueError(f"Pipeline '{name}' not found")
        
        self.logger.info(f"Running pipeline '{name}'")
        return self.pipelines[name].run(context)
    
    def run_all_pipelines(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
        """Run all pipelines"""
        results = {}
        for name, pipeline in self.pipelines.items():
            self.logger.info(f"Running pipeline '{name}'")
            try:
                results[name] = pipeline.run(context)
            except Exception as e:
                self.logger.error(f"Pipeline '{name}' failed: {str(e)}")
                results[name] = {'error': str(e)}
        return results
    
    def get_all_status(self) -> Dict[str, Any]:
        """Get status of all pipelines"""
        return {
            name: pipeline.get_status_summary()
            for name, pipeline in self.pipelines.items()
        }
