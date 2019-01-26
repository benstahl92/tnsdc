# standard imports
import pandas as pd
import io
from astroquery.ned import Ned
from astropy.coordinates import SkyCoord
from astropy import units as u
from datetime import datetime, timedelta
import requests
from urllib import request, parse
import json

# configuration
pd.options.mode.chained_assignment = None

def get_z_ned(coord = None, RA = None, DEC = None):
    '''query NED and return redshift of nearest galaxy or None if failed'''
    
    if coord is None:
        coord = SkyCoord('{} {}'.format(RA, DEC), unit=(u.hourangle, u.deg))
    
    # query ned
    result_table = Ned.query_region(coord, radius = 1 * u.arcmin)
    r = result_table.to_pandas()
    
    # select only galaxy with a redshift
    cand = r[r['Type'].isin([b'G',b'GPair',b'GTrpl',b'GGroup']) & r['Redshift'].notnull()]
    
    if len(cand) == 0:
        return None
    elif len(cand) == 1:
        return cand['Redshift'].item()
    else:
        # rank by separation and use the closest
        cand.loc[:,'sep'] = coord.separation(SkyCoord(ra = cand.loc[:,'RA(deg)'], dec = cand.loc[:,'DEC(deg)'], unit = (u.deg, u.deg)))
        return cand.sort_values(by = 'sep').iloc[0].loc['Redshift'].item()

def scrape_TNS(start, end):
	'''given start and and datetime objects, search TNS for candidate discoveries and return as DataFrame'''

	# format dates
	start = '{}-{:02}-{:02}'.format(start.year, start.month, start.day)
	end = '{}-{:02}-{:02}'.format(end.year, end.month, end.day)

	# setup search URL
	url = ('https://wis-tns.weizmann.ac.il/search?&name=&name_like=0&isTNS_AT=yes&public=all'
       '&unclassified_at=1&classified_sne=0&ra=&decl=&radius=&coords_unit=arcsec'
       '&groupid%5B%5D=null&classifier_groupid%5B%5D=null&objtype%5B%5D=null&at_type%5B%5D=null'
       '&date_start%5Bdate%5D={}&date_end%5Bdate%5D={}&discovery_mag_min=&discovery_mag_max='
       '&internal_name=&redshift_min=&redshift_max=&spectra_count=&discoverer=&classifier='
       '&discovery_instrument%5B%5D=&classification_instrument%5B%5D=&hostname='
       '&associated_groups%5B%5D=null&ext_catid=&num_page=1000&display%5Bredshift%5D=1'
       '&display%5Bhostname%5D=1&display%5Bhost_redshift%5D=1&display%5Bsource_group_name%5D=1'
       '&display%5Bclassifying_source_group_name%5D=1&display%5Bdiscovering_instrument_name%5D=0'
       '&display%5Bclassifing_instrument_name%5D=0&display%5Bprograms_name%5D=0&display%5Binternal_name%5D=1'
       '&display%5BisTNS_AT%5D=0&display%5Bpublic%5D=1&display%5Bend_pop_period%5D=0'
       '&display%5Bspectra_count%5D=0&display%5Bdiscoverymag%5D=1&display%5Bdiscmagfilter%5D=1'
       '&display%5Bdiscoverydate%5D=1&display%5Bdiscoverer%5D=0&display%5Bsources%5D=0'
       '&display%5Bbibcode%5D=1&display%5Bext_catalogs%5D=0&format=csv').format(start, end)

	# execute search
	session = requests.Session()
	information = session.get(url)
	decoded_information = information.content.decode('utf-8')
	data = decoded_information.splitlines()

	return pd.read_csv(io.StringIO('\n'.join(data)))

def slack_alert(msg, url):
    '''post <msg> to Slack channel using incoming WebHooks url'''
    
    post = {"text": msg}
    try:
        json_data = json.dumps(post)
        req = request.Request(url, data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))