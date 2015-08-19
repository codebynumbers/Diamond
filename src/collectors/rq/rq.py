# coding=utf-8
"""
The RQ collector collects metrics for all RQ queues in a redis instance

#### Configuration

Below is an example configuration for the RQCollector.
You can specify an arbitrary amount of regions

```
    enabled = True
    interval = 60

    [redis]
    host = '...'
    port = '...'
    db = '...'
```

Note: If you modify the RQCollector configuration, you will need to
restart diamond.

#### Dependencies

 * redis

"""
import diamond.collector
try:
    from redis import Redis
except ImportError:
    Redis = False


class RQCollector(diamond.collector.Collector):

    conn = None

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(RQCollector, self).get_default_config()
        config.update({
            'path': 'rq',
            })
        return config

    def collect(self):
        if not Redis:
            self.log.error("redis module not found!")
            return

        if not self.conn:
            try:
                self.conn = Redis(**self.config['redis'])
            except Exception, e:
                self.log.error("Couldn't connect to redis: %s", e)
                return

        queues = self.conn.smembers('rq:queues')
        for queue in queues:
            name = queue.replace('rq:queue:', '')
            metric_name = "queue.{}.size".format(name)
            metric_value = self.conn.llen(queue)
            self.publish(metric_name, metric_value)

