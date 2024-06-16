import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

import keepa_manager
from discount_properties import is_big_discount

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': 'analytics_channel=mcomm; _abck=F00624B0353064CB97EE9E72FB0043F3~0~YAAQL717XEstkgaQAQAA0iINHQxtGDfHhYtyOAp2UOsytM+IYmrGk6GCEQx7Vt6hzEKckNx8MqY/Z/n/RLsCF2HpJISBzVlwfayjSQ6GwyUA2v66VnlqgVP+KY+a8mWIaZ70b54fQ2WqQt4INqoqjPYzq00dAInlul7s9/OJrecFkgeYKOSuUj55Qz+tFGXKFj11thgtRzbywL/Aa7AtoPf8OWgiwccLucVNGLElPU4wbgpgWkBc+KX3Hw5qIv7nutQVKbxNmXqXwfsTzG2SZq8OFPOBgNvCp9cOBrMPSoVoSBN3Qq/xp51SAUHB+SXtQHDfs+0DGE7KmmLID4deZXHJbiNpZ+hEJJRjGuxxo4Zmf7R13A18WB3X5LWvbK8cK4ANtKcFtWeKaBuuJqPhqgZPyDvyt7xe5x840CCT/1R0QHMv4w==~-1~-1~-1; utag_main=v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:13$_se:54$_ss:0$_st:1718476121880$vapi_domain:argos.co.uk$dc_visit:13$ses_id:1718473172480%3Bexp-session$_pn:4%3Bexp-session$dc_event:48%3Bexp-session; sessionId=I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/; cisId=efc9db526d7a43d0b7747ca53d73c2c6; AMCV_095C467352782EB30A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19890%7CMCMID%7C87286231597634338936380337387751060019%7CMCAID%7CNONE%7CMCOPTOUT-1718481518s%7CNONE%7CvVersion%7C5.5.0; _cls_v=9da0bcf3-1541-4815-b22b-6738aa4b3584; _taggstar_vid=2dca6491-d708-11ee-8214-537a6449f81f; _taggstar_exp=v:3|id:|group:; umdid=NDZmZDA1NTEtZjViYS00ZDlhLTkwYzEtMGEwZTY4N2I1M2YwfGNhM2M1NTJkLWU4MjUtNDE2OS05YTliLTRjZDY3ZWJiZDBjOHww; syte_uuid=20b4f410-fd8d-11ee-829e-9557f3b9dbbe; syte_ab_tests={}; prev_vals=ar%3Apdp%3A1180778%3Aamazonkindlepaperwhitesignatureed32gbwi-fie-reader%3A*%7C*ar%3Aproductdetails%3A; AMCVS_095C467352782EB30A490D45%40AdobeOrg=1; ArgosPopUp_customer1In20Chance=false; _cls_s=83163b84-2088-4dce-b68c-dc371616079d:0; Bc=d:1*1_p:0*0.005_r:null*null; akavpau_vpc_gcd=1718474904~id=816b362b3a8f3c1f7f55decb76b18ad9; akavpau_vpc_pdpcd=1718474915~id=470299fd1e4b6655f0034cd6ee18d50e; bm_s=YAAQL717XHAtkgaQAQAAiSYNHQE1CefWitIbd2UMPGPnPXlQ2koZ6+dZrPUCnMljOCGzTBhBP0eXTp0UlOzbB9ip39eApfCthm7PGZfiKTSAFAsya9ezD+xlgwS0CwiR84iHi8VlziMR/ztEqzlHgFzaJCRGCRvlBS3H1LAkqR5B7xIIAKBTEGp8kDOQqp55hzbimwemVGoJRUxl1B+e1Xcima3hKUIyEw/yKA9ZmdZW2f33UaniksUP4+3jo14jMqhCCyp4PGapOAY+PDJvoNl+WMBTU5d8sIAvyjt08ztGcdw+Gyb7wN2gbHP1PvWvh5YH+aHJbmDejzd8TSgrsTbYdvqMOCxu; Checkout_Test_Group_2=NEW_HD|NEW_HD_SI|NEW_HD_LI; akaas_arg_uk_global=1719683917~rv=12~id=4be9a8284b15f27bd4bbe540229ba89c; localisationTooltip=open; CONSENTMGR=consent:true%7Cts:1718444037019%7Cid:018dacfc0c9c004ff4950a12766c05050005700d00bd0; PDP_Test_Group_1=2; ufvd=~abTestVariantGroup-B~clp_29203-U!brands_tommy-hilfiger-U!clp_29949-K!brands_amazon-K; mdr_browser=Akamai; ak_bmsc=9F79B96557EA2996E752686C5C7CB4BD~000000000000000000000000000000~YAAQSAcQAmgr4RmQAQAAFHz7HBje1cOVr9pteOzIO63z2+BWw/7cplV3hJAMhx+i40dFWNtgkDy4oUUL1DC/1A133tf0Ptm6yx5Fuzb2k1uIOMKhP4ebMKMFSa6dvXgQ652fnoEP6evs1y6KVUDTP90Bi/0ynbUlNc2n0UPUavmbGZeTZneHmEOZ5x3sZ90KfcemLGnnibyFDusKigiBLmNcKYu7Ntk0NwuAZk3N2n7lgdjpDJ5lNSdzQjnkmIfHPg6KoJGkDZD58pRshmmxihwIDa3v+Ux7pYQ+TTdyyViFnPzcfhmO1ucH45lXg5RLhcRs5M4SxsfxvGsv/fKLX2K0qnRMRSgjcg4QUF4Gow+yMLOPloflS3JOZDFZnzCqLO3fGpe1/rZt8UI=; AKA_A2=A; bm_ss=ab8e18ef4e; bm_mi=952E49C3193D35A93B15D2F8F9F4E6A2~YAAQL717XMUrkgaQAQAAQe0MHRiSKwubOta0q2X90EqGs+ZrFYHCZtZjXHSmC37kVPsk258XOOcMSivPCBg38Fyh2NTprzC/3TNbEQhIJmgkhrZrs+oEsPR256uoMZ41NtwbO8d8injrsBZwJimfQDZXoWIFvsueMb7Cu7OGrAf1ySlVWowO+izCWZUCxWnRlCRQCFXiFSk/lsGxmby33M9NGjompn9hN7gPuayqtxWfj6D+xYuycYqPkquuaUoU91AFMvffgYLnaU7RDrk16qmJiokHY8/o6NOLCEaCmq37tjsJMM4cp8Bjk+amYw==~1; bm_sv=612A2A65CA705A6817D7E442D53D906D~YAAQL717XH8tkgaQAQAA+ygNHRg4S2mLwz/ZPrVdP3e2QiAXrutD3fW22nSxkTLfFu3ZgOpNEAfR29K/Tc1Q3W7G/TcOj0915D6cLa1t9kLJkr5/W1U4uJQ1HmslDC3jVELDxCKHlIUXb5iibHlcowGGaNg+8ckQa84aJhoce9DaHTbJNcjZDIE1nl8b1vc9CJCEGHQpSz28L+3HIcaws+ulEh8ZmH5muFmHpMtXwWwn+iXhN8JCwOwhtz5ILo8d44w=~1; bm_sz=85066BEBE900C3D85C9465E06BE1175A~YAAQL717XPwskgaQAQAAhxYNHRhJtyel/c2n4t2vAnQexiL6DUA7Y0RmJjDmg5eKNE9/fcJaLG4i/r8l++4YacpIG2t+Gft0hU07M2XUFuyrAlqpyRfj7dNFhD7KMM64dDMhndJWUw4GpfgtDCKXjdMX/m0j2s+J4it48wIMOYsX6AXJPgyboSO61VM+w3jjUiCJ7H+fWkf4cqIo9QR679RsOoj0e5KiYUSzLnLv3wXR33UY/AHfesAiZhTkasPhBYKufrevJSoxipIyX/ScF0lbGw40O5HKzhWAtMz4UteJ7KA3YfTpsowxojyu7cGH/nEEOL+R1zO0qRC1XSlrgYeQLYaI1qwGJ+9uIKEeq4cn6MSVy3THKbgyke5Rnb9qvHBmGlSA3R+isbn35aRHvPigZRKyhtiOnJOA1Foj3tYZ5PPBUo147vI=~4473397~4272439; stimgs={%22sessionId%22:73477779%2C%22didReportCameraImpression%22:false%2C%22newUser%22:false}; _taggstar_ses=424fb4f8-2b3e-11ef-be80-31b7cc44d6fa; AWSALB=Rk1VKfxNMllsVC/u31S6SaUSovbdWnGMNHjiNabw63H0R8JHfYBGfwVzZj7e7caifyF9KzegDrVG7hUxMGJQ6TuYxANgjMBfZjfLWtj2v7JaANKTwe9liFFHsJ8P; AWSALBCORS=Rk1VKfxNMllsVC/u31S6SaUSovbdWnGMNHjiNabw63H0R8JHfYBGfwVzZj7e7caifyF9KzegDrVG7hUxMGJQ6TuYxANgjMBfZjfLWtj2v7JaANKTwe9liFFHsJ8P; Apache=10.102.16.99.1718473615020850; JSESSIONID=0000sS190TFnLLdcHPuZJBgeWJ6:1fa26qr2o; WC_PERSISTENT=k6Qd2x2WxBW0ZhnGixOTBe9tXew%3D%0A%3B2024-06-15+18%3A58%3A14.782_1718473615021-776277_10151; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_13907625476=13907625476%2C0qUMC3p%2FChOrzhx%2Ber6JGyRp3MI%3D; WC_ACTIVEPOINTER=110%2C10151; WC_USERACTIVITY_13907625476=13907625476%2C10151%2Cnull%2Cnull%2C1718474294782%2C1718476094782%2Cnull%2Cnull%2Cnull%2Cnull%2CpPgnohA03xuUrkdYVffXAZ8b15u4HQ1tZIHEI%2FQUmuWrBqrn5lGIlJemtZ43bT2k1lt%2BRrk8i8PQNHrUomOvQYTEX8BmKUiuPmVidweKYLiNVrL8WkHM0IP6bAjwRRCLqkQ3b2ZSBhq54JIm%2FfQhRLV%2FK%2BoX9s%2BTHvO1%2Fnb81ykeshg4fSBU4%2FAXLbMI7We%2FDL562QTZonH3FemyBHI6im0ZRgzih%2BqV191h9XWCRNajgxElIk5za0vbKZ0nvewO; pwd_email=new; UserPersistentSessionCookie=13907625476%3BQous%3BLOGGEDIN%3BloggedIn%3BGIFT_NO%3B10.102.16.99.1718473615020850%3BREMEMBER_NO%3B%3Bfalse%3B; PostCodeSessionCookie=%2CM11AA%2C; UserRegistrationType=R; akaas_arg_uk_pm_dxc=100; Content_Test_Group_1=2; argos_cis_delay_refresh=true; sids=WyI2NjEiXQ%3D%3D'
}

cookies = {
    '_abck': 'F00624B0353064CB97EE9E72FB0043F3~0~YAAQL717XEstkgaQAQAA0iINHQxtGDfHhYtyOAp2UOsytM+IYmrGk6GCEQx7Vt6hzEKckNx8MqY/Z/n/RLsCF2HpJISBzVlwfayjSQ6GwyUA2v66VnlqgVP+KY+a8mWIaZ70b54fQ2WqQt4INqoqjPYzq00dAInlul7s9/OJrecFkgeYKOSuUj55Qz+tFGXKFj11thgtRzbywL/Aa7AtoPf8OWgiwccLucVNGLElPU4wbgpgWkBc+KX3Hw5qIv7nutQVKbxNmXqXwfsTzG2SZq8OFPOBgNvCp9cOBrMPSoVoSBN3Qq/xp51SAUHB+SXtQHDfs+0DGE7KmmLID4deZXHJbiNpZ+hEJJRjGuxxo4Zmf7R13A18WB3X5LWvbK8cK4ANtKcFtWeKaBuuJqPhqgZPyDvyt7xe5x840CCT/1R0QHMv4w==~-1~-1~-1',
    '_cls_s': '83163b84-2088-4dce-b68c-dc371616079d:0',
    '_cls_v': '9da0bcf3-1541-4815-b22b-6738aa4b3584',
    '_taggstar_exp': 'v:3|id:|group:',
    '_taggstar_ses': '424fb4f8-2b3e-11ef-be80-31b7cc44d6fa',
    '_taggstar_vid': '2dca6491-d708-11ee-8214-537a6449f81f',
    'ak_bmsc': '9F79B96557EA2996E752686C5C7CB4BD~000000000000000000000000000000~YAAQSAcQAmgr4RmQAQAAFHz7HBje1cOVr9pteOzIO63z2+BWw/7cplV3hJAMhx+i40dFWNtgkDy4oUUL1DC/1A133tf0Ptm6yx5Fuzb2k1uIOMKhP4ebMKMFSa6dvXgQ652fnoEP6evs1y6KVUDTP90Bi/0ynbUlNc2n0UPUavmbGZeTZneHmEOZ5x3sZ90KfcemLGnnibyFDusKigiBLmNcKYu7Ntk0NwuAZk3N2n7lgdjpDJ5lNSdzQjnkmIfHPg6KoJGkDZD58pRshmmxihwIDa3v+Ux7pYQ+TTdyyViFnPzcfhmO1ucH45lXg5RLhcRs5M4SxsfxvGsv/fKLX2K0qnRMRSgjcg4QUF4Gow+yMLOPloflS3JOZDFZnzCqLO3fGpe1/rZt8UI=',
    'AKA_A2': 'A',
    'akaas_arg_uk_global': '1719683917~rv=12~id=4be9a8284b15f27bd4bbe540229ba89c',
    'akaas_arg_uk_pm_dxc': '100',
    'akavpau_vpc_gcd': '1718474904~id=816b362b3a8f3c1f7f55decb76b18ad9',
    'akavpau_vpc_pdpcd': '1718474915~id=470299fd1e4b6655f0034cd6ee18d50e',
    'AMCV_095C467352782EB30A490D45@AdobeOrg': '179643557|MCIDTS|19890|MCMID|87286231597634338936380337387751060019|MCAID|NONE|MCOPTOUT-1718481518s|NONE|vVersion|5.5.0',
    'AMCVS_095C467352782EB30A490D45@AdobeOrg': '1',
    'analytics_channel': 'mcomm',
    'Apache': '10.102.16.99.1718473615020850',
    'argos_cis_delay_refresh': 'true',
    'ArgosPopUp_customer1In20Chance': 'false',
    'AWSALB': 'Rk1VKfxNMllsVC/u31S6SaUSovbdWnGMNHjiNabw63H0R8JHfYBGfwVzZj7e7caifyF9KzegDrVG7hUxMGJQ6TuYxANgjMBfZjfLWtj2v7JaANKTwe9liFFHsJ8P',
    'AWSALBCORS': 'Rk1VKfxNMllsVC/u31S6SaUSovbdWnGMNHjiNabw63H0R8JHfYBGfwVzZj7e7caifyF9KzegDrVG7hUxMGJQ6TuYxANgjMBfZjfLWtj2v7JaANKTwe9liFFHsJ8P',
    'Bc': 'd:1*1_p:0*0.005_r:null*null',
    'bm_mi': '952E49C3193D35A93B15D2F8F9F4E6A2~YAAQL717XMUrkgaQAQAAQe0MHRiSKwubOta0q2X90EqGs+ZrFYHCZtZjXHSmC37kVPsk258XOOcMSivPCBg38Fyh2NTprzC/3TNbEQhIJmgkhrZrs+oEsPR256uoMZ41NtwbO8d8injrsBZwJimfQDZXoWIFvsueMb7Cu7OGrAf1ySlVWowO+izCWZUCxWnRlCRQCFXiFSk/lsGxmby33M9NGjompn9hN7gPuayqtxWfj6D+xYuycYqPkquuaUoU91AFMvffgYLnaU7RDrk16qmJiokHY8/o6NOLCEaCmq37tjsJMM4cp8Bjk+amYw==~1',
    'bm_s': 'YAAQL717XHAtkgaQAQAAiSYNHQE1CefWitIbd2UMPGPnPXlQ2koZ6+dZrPUCnMljOCGzTBhBP0eXTp0UlOzbB9ip39eApfCthm7PGZfiKTSAFAsya9ezD+xlgwS0CwiR84iHi8VlziMR/ztEqzlHgFzaJCRGCRvlBS3H1LAkqR5B7xIIAKBTEGp8kDOQqp55hzbimwemVGoJRUxl1B+e1Xcima3hKUIyEw/yKA9ZmdZW2f33UaniksUP4+3jo14jMqhCCyp4PGapOAY+PDJvoNl+WMBTU5d8sIAvyjt08ztGcdw+Gyb7wN2gbHP1PvWvh5YH+aHJbmDejzd8TSgrsTbYdvqMOCxu',
    'bm_ss': 'ab8e18ef4e',
    'bm_sv': '612A2A65CA705A6817D7E442D53D906D~YAAQL717XH8tkgaQAQAA+ygNHRg4S2mLwz/ZPrVdP3e2QiAXrutD3fW22nSxkTLfFu3ZgOpNEAfR29K/Tc1Q3W7G/TcOj0915D6cLa1t9kLJkr5/W1U4uJQ1HmslDC3jVELDxCKHlIUXb5iibHlcowGGaNg+8ckQa84aJhoce9DaHTbJNcjZDIE1nl8b1vc9CJCEGHQpSz28L+3HIcaws+ulEh8ZmH5muFmHpMtXwWwn+iXhN8JCwOwhtz5ILo8d44w=~1',
    'bm_sz': '85066BEBE900C3D85C9465E06BE1175A~YAAQL717XPwskgaQAQAAhxYNHRhJtyel/c2n4t2vAnQexiL6DUA7Y0RmJjDmg5eKNE9/fcJaLG4i/r8l++4YacpIG2t+Gft0hU07M2XUFuyrAlqpyRfj7dNFhD7KMM64dDMhndJWUw4GpfgtDCKXjdMX/m0j2s+J4it48wIMOYsX6AXJPgyboSO61VM+w3jjUiCJ7H+fWkf4cqIo9QR679RsOoj0e5KiYUSzLnLv3wXR33UY/AHfesAiZhTkasPhBYKufrevJSoxipIyX/ScF0lbGw40O5HKzhWAtMz4UteJ7KA3YfTpsowxojyu7cGH/nEEOL+R1zO0qRC1XSlrgYeQLYaI1qwGJ+9uIKEeq4cn6MSVy3THKbgyke5Rnb9qvHBmGlSA3R+isbn35aRHvPigZRKyhtiOnJOA1Foj3tYZ5PPBUo147vI=~4473397~4272439',
    'Checkout_Test_Group_2': 'NEW_HD|NEW_HD_SI|NEW_HD_LI',
    'cisId': 'efc9db526d7a43d0b7747ca53d73c2c6',
    'CONSENTMGR': 'consent:true|ts:1718444037019|id:018dacfc0c9c004ff4950a12766c05050005700d00bd0',
    'Content_Test_Group_1': '2',
    'JSESSIONID': '0000sS190TFnLLdcHPuZJBgeWJ6:1fa26qr2o',
    'localisationTooltip': 'open',
    'mdr_browser': 'Akamai',
    'PDP_Test_Group_1': '2',
    'PostCodeSessionCookie': ',M11AA,',
    'prev_vals': 'ar:pdp:1180778:amazonkindlepaperwhitesignatureed32gbwi-fie-reader:*|*ar:productdetails:',
    'pwd_email': 'new',
    'sessionId': 'I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/',
    'sids': 'WyI2NjEiXQ==',
    'stimgs': '{"sessionId":73477779,"didReportCameraImpression":false,"newUser":false}',
    'syte_ab_tests': '{}',
    'syte_uuid': '20b4f410-fd8d-11ee-829e-9557f3b9dbbe',
    'ufvd': '~abTestVariantGroup-B~clp_29203-U!brands_tommy-hilfiger-U!clp_29949-K!brands_amazon-K',
    'umdid': 'NDZmZDA1NTEtZjViYS00ZDlhLTkwYzEtMGEwZTY4N2I1M2YwfGNhM2M1NTJkLWU4MjUtNDE2OS05YTliLTRjZDY3ZWJiZDBjOHww',
    'UserPersistentSessionCookie': '13907625476;Qous;LOGGEDIN;loggedIn;GIFT_NO;10.102.16.99.1718473615020850;REMEMBER_NO;;false;',
    'UserRegistrationType': 'R',
    'utag_main': 'v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:13$_se:54$_ss:0$_st:1718476121880$vapi_domain:argos.co.uk$dc_visit:13$ses_id:1718473172480;exp-session$_pn:4;exp-session$dc_event:48;exp-session',
    'WC_ACTIVEPOINTER': '110,10151',
    'WC_AUTHENTICATION_13907625476': '13907625476,0qUMC3p/ChOrzhx+er6JGyRp3MI=',
    'WC_PERSISTENT': 'k6Qd2x2WxBW0ZhnGixOTBe9tXew=\n;2024-06-15+18:58:14.782_1718473615021-776277_10151',
    'WC_SESSION_ESTABLISHED': 'true',
    'WC_USERACTIVITY_13907625476': '13907625476,10151,null,null,1718474294782,1718476094782,null,null,null,null,pPgnohA03xuUrkdYVffXAZ8b15u4HQ1tZIHEI/QUmuWrBqrn5lGIlJemtZ43bT2k1lt+Rrk8i8PQNHrUomOvQYTEX8BmKUiuPmVidweKYLiNVrL8WkHM0IP6bAjwRRCLqkQ3b2ZSBhq54JIm/fQhRLV/K+oX9s+THvO1/nb81ykeshg4fSBU4/AXLbMI7We/DL562QTZonH3FemyBHI6im0ZRgzih+qV191h9XWCRNajgxElIk5za0vbKZ0nvewO'
}

prices = {}

temporary_discounts = {}


def get_new_prices(url, page_number=1):
    response = requests.get(url+f"opt/page:{page_number}/", headers=header)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('div', class_='ProductCardstyles__ContentBlock-h52kot-5')

        discounts_list = []
        for item in items:
            name = item.find('div', class_='ProductCardstyles__Title-h52kot-12').text.strip()
            price = float(item.find('div', class_='ProductCardstyles__PriceText-h52kot-16').text.strip().replace("£", ""))
            old_price = item.find("div", class_="ProductCardstyles__WasText-h52kot-20")
            if old_price:
                old_price = float(old_price.text.replace("Was", "").strip().replace("£", ""))
            else:
                old_price = price
            link = "https://www.argos.co.uk" + item.find('a', class_='ProductCardstyles__Link-h52kot-13')['href'].split("?")[0]
            image = f"https://media.4rgos.it/s/Argos/{link.split('/')[4].split('?')[0]}_R_SET?w=270&h=270&qlt=75&fmt.jpeg.interlaced=true"

            item_data = {
                "name": name,
                "price": price,
                "link": link,
                "old_price": old_price,
                "image": image
            }
            if link in prices:
                item_data["old_price"] = prices[link]["old_price"]
                if prices[link]["old_price"] > price and price != prices[link]["price"] and link not in temporary_discounts:
                    item_data["old_price"] = prices[link]["old_price"]
                    item_data["previous_price"] = prices[link]["price"]
                    prices[link]["price"] = price
                    discounts_list.append(item_data)
                    temporary_discounts[link] = datetime.now()
                elif link not in temporary_discounts:
                    if prices[link]["old_price"] < old_price:
                        prices[link]["old_price"] = old_price
                    prices[link]["price"] = price
            else:
                prices[link] = item_data.copy()
                item_data["old_price"] = 0
                discounts_list.append(item_data)

        item_count = int(soup.find("span", class_="styles__ResultsCount-sc-1hkcas-11")["data-search-results"])
        if 60*page_number < item_count:
            time.sleep(1)
            for discount in get_new_prices(url,page_number+1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve argos page")
        return []


def get_keepa_results(price_drops):
    keepa_drops = []
    for price_drop in price_drops:
        if price_drop["old_price"] == 0 or price_drop["price"]/price_drop["previous_price"] <= 0.85:
            bar_code = get_bar_code(price_drop["link"])
            if not bar_code:
                compare_price, fee, fee_percentage, asin, avg90 = keepa_manager.get_from_title(price_drop["name"])
            else:
                compare_price, fee, fee_percentage,asin,avg90 = keepa_manager.get_from_bar_code(bar_code)

            if not compare_price:
                continue
            profit = compare_price-price_drop["price"]-0.5-(compare_price/6 - price_drop["price"]/6) - fee - (compare_price*fee_percentage)
            profit_margin = profit/compare_price
            if profit_margin >= 0.15:
                margin_ping = {
                    "keepa_price": compare_price,
                    "price": price_drop["price"],
                    "name": price_drop["name"],
                    "link": price_drop["link"],
                    "margin": profit_margin,
                    "ASIN":asin,
                    "avg": avg90,
                    "image": price_drop["image"]
                }
                keepa_drops.append(margin_ping)
    return keepa_drops


def get_bar_code(link):
    response = requests.get(link, headers=header, cookies=cookies, impersonate="chrome120")
    soup = BeautifulSoup(response.content, 'html.parser')
    description = soup.find("div", class_="product-description-content-text")
    lines = description.find_all("li")
    if len(lines) > 0 and "EAN:" in lines[len(lines)-1].text:
        return lines[len(lines)-1].text.replace("EAN:", "").replace(".", "").strip()
    return None

