from classopt import classopt
from wikibaseintegrator import WikibaseIntegrator, wbi_login, datatypes
from wikibaseintegrator.wbi_config import config


@classopt(default_long=True)
class CLIOpt:
    qid: str
    username: str
    password: str

MEDIA_FRANCHISE_QID="Q196600"
MEDIA_FRANCHISE_PID="P8345"
CLASSIFICATION_PID="P31"
HAS_PART_PID="P527"

if __name__ == "__main__":
    args = CLIOpt.from_args()

    config["USER_AGENT"] = "'MyWikibaseBot/1.0 (https://www.wikidata.org/wiki/User:Eniehack)"
    wbi = WikibaseIntegrator()

    login_wikidata = wbi_login.Login(user=args.username, password=args.password, mediawiki_api_url='https://www.wikidata.org/w/api.php')

    entity = wbi.item.get(args.qid, mediawiki_api_url='https://www.wikidata.org/w/api.php', login=login_wikidata)
    classifications = [claim.mainsnak.datavalue["value"]["id"] for claim in entity.claims.get(CLASSIFICATION_PID)]
    if MEDIA_FRANCHISE_QID not in classifications:
        exit(1)

    spin_offs = [claim.mainsnak.datavalue["value"]["id"] for claim in entity.claims.get(HAS_PART_PID)]
    for q in spin_offs:
        entity = wbi.item.get(q, mediawiki_api_url='https://www.wikidata.org/w/api.php', login=login_wikidata)
        mediafranchises = [claim.mainsnak.datavalue["value"]["id"] for claim in entity.claims.get(MEDIA_FRANCHISE_PID)]
        if args.qid in mediafranchises:
            continue
        entity.claims.add(datatypes.Item(prop_nr=MEDIA_FRANCHISE_PID, value=args.qid))
        entity.write(login=login_wikidata)
