import ast
import redis
import json
import re
import traceback
from datetime import datetime, timedelta

from django.conf import settings

from crm.config import PARAM_DICT
from network.settings import DEFAULT_HASH_KEY

class AccessRedisData(object):
    def __init__(self):
        self.r_conn_slave = redis.StrictRedis(host=settings.REDIS_SLAVE_IP[settings.ENV], port=settings.REDIS_PORT, db=0)
        self.r_conn_master = redis.StrictRedis(host=settings.REDIS_MASTER_IP[settings.ENV], port=settings.REDIS_PORT, db=0)

    def get_value(self, key):
        return self.r_conn_slave.get(key)

    def set_value(self, key, value, ttl=None):
        """
        in exiting flow, lot of places dump into redis through ast, this causes inconsistency
        while dumping the data in redis.
        To meake this consistent, we identify the redis value to be dumped and if it is of type
        dict, we ensure it is of python compatible json format

        :param key: key, redis key
        :param value: redis value to be dumped
        :param ttl: optional, time when data shud expire from time of dump ( in seconds )
        :return: None
        """
        try:
            redis_val = value
            if isinstance(value, str):
                try:
                    redis_val = json.dumps(json.loads(value))
                except Exception as e:
                    try:
                        redis_val = ast.literal_eval(value)
                        if isinstance(redis_val, dict):
                            redis_val = json.dumps(redis_val)
                        else:
                            redis_val = str(value)
                    except Exception as e:
                        redis_val = value
            if ttl:
                if type(ttl) is int and ttl > 0:
                    self.r_conn_master.set(key, redis_val)
                    self.r_conn_master.expire(key, ttl)
                else:
                    raise Exception("ttl has to be int, with value > 0 ", type(ttl), " sent")
            else:
                self.r_conn_master.set(key, redis_val)
        except Exception as e:
            formatted_lines = traceback.format_exc().splitlines()
            print "error in set_value in access redis data ", formatted_lines

    def hset_value(self, r_key, r_value, hash_key=None):
        try:
            if not hash_key:
                hash_key = DEFAULT_HASH_KEY
            self.r_conn_master.hset(hash_key, r_key, r_value)
        except Exception as e:
            print "Error in setting hash key-value in redis: %s" % (str(e))

    def set_value_to_expire_midnight(self, key, value):
        try:
            now = datetime.now()
            midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            ttl_sec = (midnight - now).seconds
            self.set_value(key, value, ttl=ttl_sec)
        except:
            formatted_lines = traceback.format_exc().splitlines()
            print "error in set_value_to_expire_midnight in access redis data ", formatted_lines

    def hget_value(self, r_key=None, hash_key=None):
        try:
            clean_dict, r_value = {}, {}
            h_key = DEFAULT_HASH_KEY if not hash_key else hash_key
            if r_key:
                r_value = self.r_conn_slave.hget(h_key, r_key)
                if r_value:
                    clean_dict = ast.literal_eval(r_value)
            else:
                r_value = self.r_conn_slave.hgetall(h_key)
                for key in r_value:
                    clean_dict[key] = ast.literal_eval(r_value.get(key))
        except Exception as e:
            clean_dict = r_value
            print "Error in getting hash value from redis: %s" % (str(e))
        return clean_dict

    def hdelete_value(self, hash_key, key):
        try:
            return self.r_conn_master.hdel(hash_key, key)
        except Exception as e:
            print "error delete hkey : ", e
            return False

    def hdelete_all_keys_of_pattern(self, hash_key, pattern):
        try:
            regex = re.compile(pattern)
            deleted_keys = "#"
            for key in self.r_conn_slave.hgetall(hash_key):
                if regex.match(key):
                    deleted_keys += key + "#"
                    self.hdelete_value(hash_key, key)
            return True
        except Exception as e:
            print "error in hdelete_all_keys_of_pattern : ", e
            return False

    def hget_all_keys_of_pattern(self, hash_key, pattern):
        try:
            pattern_list = []
            regex = re.compile(pattern)
            for key in self.r_conn_slave.hgetall(hash_key):
                if regex.match(key):
                    pattern_list.append(key)
        except Exception as e:
            pattern_list = []
            print "error in hget_all_keys_of_pattern : ", e
        return pattern_list

    def delete_value(self, key):
        try:
            self.r_conn_master.delete(key)
            status = True
        except Exception as e:
            print "Error in deleting key from redis: %s" % (str(e))
            status = False
        return status

    def delete_all_keys_of_pattern(self, pattern):
        try:
            for r_key in self.r_conn_master.keys(pattern=pattern):
                self.r_conn_master.delete(r_key)
                print "deleted ", r_key
        except Exception as e:
            print "Exception in delete_all_keys_of_pattern : ", e.message

    def get_all_keys_of_pattern(self, pattern):
        pattern_list = []
        try:
            for r_key in self.r_conn_slave.keys(pattern=pattern):
                pattern_list.append(r_key)
        except:
            pattern_list = []
        return pattern_list

    def get_group_id_from_param(self, param):
        details = None
        try:
            details = self.r_conn_slave.get(param)
            if details:
                details = ast.literal_eval(details)
                return details['group_id']
        except:
            pass
        return details

    def get_group_metadata(self, group_id):
        try:
            group_stats = self.r_conn_slave.get(group_id + "_stats")
            if group_stats:
                return ast.literal_eval(group_stats)
        except:
            pass
        return {}

    def get_group_stat(self, group_id):
        try:
            return self.hget_value(hash_key=group_id)
        except:
            pass
        return {}

    def get_txndata_dict_for_txns(self, txnlist):
        stats_dict = {}
        for txn in txnlist:
            data = self.r_conn_slave.get(txn)
            if data:
                data = ast.literal_eval(data)
                stats_dict[txn] = data
        return stats_dict

    def get_last_thirty_days_stat(self, param_name,param_value):
        param_value = param_value.replace('.', '').replace('@', '')  # re.sub('[.!@#$]', '',param_value)
        param_value = param_value.strip()
        # redis_keys = PARAM_DICT[param_name]
        redis_keys = PARAM_DICT[param_name] if param_name in PARAM_DICT else param_name
        for loop_variable in redis_keys:
            param_value = "M" + loop_variable + param_value
            last_month_data = self.hget_value(hash_key=param_value)
            if last_month_data:
                return last_month_data
            param_value = ""
        return {}

    def get_param_stats(self, param):
        try:
            param_stats = None
            param_stats = self.get_value(param)
            if param_stats:
                param_stats = ast.literal_eval(param_stats)
        except Exception as e:
            if "WRONGTYPE" in e.message:
                param_stats = self.hget_value(hash_key=param)
        return param_stats

    def get_em_stats(self, em):
        em_stats = self.r_conn_slave.get(em)
        return ast.literal_eval(em_stats)

    def get_all_txn_details_in_group(self, group_id):
        group_metadata = self.hget_value(hash_key=group_id)
        stat_dict = {}
        if group_metadata:
            txnid_list = group_metadata['transactions']
            for txnid in txnid_list:
                txnid_stat = self.get_param_stats(txnid)
                if txnid_stat:
                    stat_dict.update({txnid: txnid_stat})
        return stat_dict

    def get_all_bad_networks(self):
        gids = self.get_all_keys_of_pattern('gid_*')
        for gid in gids:
            if not gid.endswith('stats'):
                meta = self.get_group_metadata(gid)
                if isinstance(meta, dict) and meta != {} and 'network_score' in meta:
                    scr = meta.get('network_score')
                    if 0 < scr < 31:
                        print gid, " : ", meta['network_score']
                        print self.get_group_stat(gid)
                        print "\n"

    def get_txn_count_of_the_date(self, vertical, date):
        # Date format shud be DD-MM-YYYY
        # vertical acceptable : "flights", "hotels", "bus", "payments"
        # sample key : hotels_count_02-11-2016
        key = vertical + "_count_" + date
        cnt = 0
        data = self.hget_value(hash_key=key)
        for key in data:
            cnt += 1
        return cnt



