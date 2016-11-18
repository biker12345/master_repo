import psycopg2
from datetime import datetime,timedelta
import traceback
from crm.helpers import send_notify_mail

class RedashUtils(object):
    def __init__(self):
        self.conn_string =  "dbname='goibibo' port='5439' \
                            user='rawreadonly' password='xfVoJ6tsarRBh7k0WS' \
                            host='dp.cvvaoavvg9r3.ap-south-1.redshift.amazonaws.com' "
        self.conn = psycopg2.connect(self.conn_string)
        self.cur = self.conn.cursor()

    def get_range_based_booking_data(self,vhid,date_range):
        start_time = (datetime.now() - timedelta(days=date_range)).strftime('%Y%m%d')
        end_time = datetime.now().strftime('%Y%m%d')
        if not vhid or not vhid.isdigit():
            return 0 
        try:
            query =  " select "
            query += " count(transactionid) "
            query += " from bookings.hotels where status='to deliver' and days >= " + start_time + " and days < " + end_time
            query += " and voyagerhotelid =" + str(vhid)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for count, in rows:
                return count
        except Exception as e :
            msg = traceback.format_exc().splitlines()
            send_notify_mail("Error in getting range wise data", msg)

    def get_txnid_with_star_rating(self,vhid,date_range):
        start_time = (datetime.now() - timedelta(days=int(date_range))).strftime('%Y%m%d')
        end_time = datetime.now().strftime('%Y%m%d')
        response_dict = {}
        txnid_list = []
        if not vhid or not vhid.isdigit():
            return {}
        try:
            query = " select "
            query += " transactionid "
            query += " from bookings.hotels where status='to deliver' and days >= " + start_time + " and days < " + end_time
            query += " and voyagerhotelid =" + str(vhid)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for count, in rows :
                txnid_list.append(count)
            response_dict['txn_id'] = txnid_list
            query = " select "
            query += " starrating "
            query += " from goibibo_inventory.hotels_hoteldetail where "
            query += " voyagerid =" + str(vhid)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for count, in rows :
                response_dict['star_rating'] = count

            query = " select "
            query += " amount "
            query += " from bookings.hotels where "
            query += " voyagerhotelid =" + str(vhid) + " and status = 'to deliver' and days= " + str(datetime.now().strftime('%Y%m%d')) 
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for count, in rows :
                response_dict['amount'] = count
        except Exception as e:
            msg = traceback.format_exc().splitlines()
            send_notify_mail("Error in getting txnid and star rating", msg)
            response_dict = {}
        return response_dict

    def get_vhid_based_inventory(self,vhid):
        try :
            if not vhid or not vhid.isdigit():
                return 0
            query = " select "
            query += " noofrooms "
            query += " from goibibo_inventory.hotels_hoteldetail "
            query += " where  voyagerid =" + str(vhid)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for count, in rows :
                return count
        except Exception as e :
            msg = traceback.format_exc().splitlines()
            send_notify_mail("Error in getting vhid based inventory", msg)


    def get_date_range_based_checkin_count(self,vhid,date_range):
        start_time = (datetime.now() - timedelta(days=int(date_range))).strftime('%Y%m%d')
        end_time = datetime.now().strftime('%Y%m%d')
        response_list = []
        if not vhid or not vhid.isdigit():
            return [] 
        try :
            query  = " select count(checkin) "
            query += " from bookings.hotels where voyagerhotelid = " +str(vhid)
            query += " and days >= " + start_time + " and days <" + end_time + " group by days " 
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for count, in rows :
                response_list.append(int(count))
        except Exception as e :
            msg = traceback.format_exc().splitlines()
            send_notify_mail("Error in getting checkin data ")
            response_list = []

        return response_list 









