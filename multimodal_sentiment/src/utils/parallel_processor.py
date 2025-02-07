import dask
from dask.distributed import Client, LocalCluster
from typing import Callable, List, Dict, Any
import numpy as np
import logging
from functools import partial

class DaskParallelProcessor:
    """Parallel processing manager using Dask"""
    
    def __init__(self, n_workers: int = None):
        self.n_workers = n_workers
        self.client = None
        self.logger = logging.getLogger(__name__)
        
    def __enter__(self):
        self.start_cluster()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
        
    def start_cluster(self):
        """Start Dask local cluster"""
        try:
            cluster = LocalCluster(n_workers=self.n_workers)
            self.client = Client(cluster)
            self.logger.info(f"Started Dask cluster with {len(self.client.scheduler_info()['workers'])} workers")
        except Exception as e:
            self.logger.error(f"Failed to start Dask cluster: {str(e)}")
            raise
            
    def shutdown(self):
        """Shutdown Dask cluster"""
        if self.client:
            self.client.close()
            self.client = None
            
    def process_frames(self, frames: List[np.ndarray], process_func: Callable, 
                      batch_size: int = 10) -> List[Dict]:
        """Process video frames in parallel"""
        if not self.client:
            self.start_cluster()
            
        # Create dask array from frames
        dask_frames = dask.array.from_array(np.array(frames), chunks=batch_size)
        
        # Create delayed computation for each batch
        delayed_results = []
        for i in range(0, len(frames), batch_size):
            batch = dask_frames[i:i+batch_size]
            delayed_result = dask.delayed(process_func)(batch)
            delayed_results.append(delayed_result)
            
        # Compute all results
        try:
            results = dask.compute(*delayed_results)
            # Flatten results if needed
            flat_results = [item for sublist in results for item in (sublist if isinstance(sublist, list) else [sublist])]
            return flat_results
        except Exception as e:
            self.logger.error(f"Error in parallel processing: {str(e)}")
            raise

class BatchProcessor:
    """Helper class for batch processing with Dask"""
    
    @staticmethod
    def create_batches(items: List[Any], batch_size: int) -> List[List[Any]]:
        """Split items into batches"""
        return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
        
    @staticmethod
    def process_batch_with_retries(batch: List[Any], process_func: Callable,
                                 max_retries: int = 3) -> List[Dict]:
        """Process a batch with retry mechanism"""
        for attempt in range(max_retries):
            try:
                results = [process_func(item) for item in batch]
                return results
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logging.warning(f"Batch processing failed, attempt {attempt + 1}/{max_retries}")
                continue
                
    @staticmethod
    def merge_batch_results(batch_results: List[List[Dict]]) -> List[Dict]:
        """Merge results from multiple batches"""
        return [item for batch in batch_results for item in batch]

class AsyncBatchProcessor:
    """Asynchronous batch processor for Dask"""
    
    def __init__(self, client: Client):
        self.client = client
        
    async def process_batch_async(self, batch: List[Any], process_func: Callable) -> List[Dict]:
        """Process a batch asynchronously"""
        futures = []
        for item in batch:
            future = self.client.submit(process_func, item)
            futures.append(future)
            
        results = await self.client.gather(futures)
        return results
        
    async def process_all_async(self, items: List[Any], process_func: Callable,
                              batch_size: int = 10) -> List[Dict]:
        """Process all items asynchronously in batches"""
        batches = BatchProcessor.create_batches(items, batch_size)
        all_results = []
        
        for batch in batches:
            batch_results = await self.process_batch_async(batch, process_func)
            all_results.extend(batch_results)
            
        return all_results
