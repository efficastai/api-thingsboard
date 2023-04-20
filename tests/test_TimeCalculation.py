from app.TimeCalculation import *


def test_calculate_time_values():
    """
    REVISAR ESTE TEST. Los valores de salida simulados no son correcots. Necesito conocer el resultado de antemano
    """
    tc = TimeCalculation()
    pya_tuple = [(1, 1681983371000), (1, 1681983491000), (1, 1681983461000), (1, 1681983431000), (1, 1681983401000),
                 (1, 1681983702000), (1, 1681983672000), (1, 1681983642000), (1, 1681983732000), (1, 1681983341000),
                 (1, 1681983311000), (1, 1681983281000), (1, 1681983582000), (1, 1681983612000), (1, 1681983552000),
                 (1, 1681983522000), (1, 1681983822000), (1, 1681983792000), (1, 1681983762000), (1, 1681983852000),
                 (1, 1681984063000), (1, 1681984032000), (1, 1681984002000), (1, 1681984183000), (1, 1681984153000),
                 (1, 1681984123000), (1, 1681984093000), (1, 1681983942000), (1, 1681983912000), (1, 1681984213000),
                 (1, 1681985567000), (1, 1681984995000), (1, 1681984965000), (1, 1681984754000), (1, 1681984724000),
                 (1, 1681985537000), (1, 1681985507000), (1, 1681983882000), (1, 1681983972000), (1, 1681984393000),
                 (1, 1681984363000), (1, 1681984333000), (1, 1681984423000), (1, 1681984454000), (1, 1681984514000),
                 (1, 1681984484000), (1, 1681984303000), (1, 1681984273000), (1, 1681984243000), (1, 1681985296000),
                 (1, 1681985266000), (1, 1681985236000), (1, 1681984544000), (1, 1681984634000), (1, 1681984604000),
                 (1, 1681984574000), (1, 1681984664000), (1, 1681984694000), (1, 1681984785000), (1, 1681984815000),
                 (1, 1681984875000), (1, 1681984845000), (1, 1681984935000), (1, 1681985326000), (1, 1681985116000),
                 (1, 1681985084000), (1, 1681985055000), (1, 1681985025000), (1, 1681985447000), (1, 1681985417000),
                 (1, 1681985386000), (1, 1681985356000), (1, 1681987102000), (1, 1681987072000), (1, 1681987042000),
                 (1, 1681988185000), (1, 1681985477000), (1, 1681984905000), (1, 1681985687000), (1, 1681985657000),
                 (1, 1681985626000), (1, 1681985597000), (1, 1681985808000), (1, 1681985778000), (1, 1681985748000),
                 (1, 1681985718000), (1, 1681985928000), (1, 1681985898000), (1, 1681985868000), (1, 1681985838000),
                 (1, 1681985146000), (1, 1681985206000), (1, 1681985176000), (1, 1681986049000), (1, 1681986018000),
                 (1, 1681985988000), (1, 1681985958000), (1, 1681986169000), (1, 1681986139000), (1, 1681986109000),
                 (1, 1681986079000), (1, 1681986259000), (1, 1681986229000), (1, 1681986199000), (1, 1681986410000),
                 (1, 1681986500000), (1, 1681986470000), (1, 1681986440000), (1, 1681986530000), (1, 1681986650000),
                 (1, 1681986620000), (1, 1681986590000), (1, 1681986560000), (1, 1681986771000), (1, 1681986741000),
                 (1, 1681986711000), (1, 1681986681000), (1, 1681986289000), (1, 1681986380000), (1, 1681986350000),
                 (1, 1681986319000), (1, 1681988065000), (1, 1681988035000), (1, 1681988005000), (1, 1681987974000),
                 (1, 1681987553000), (1, 1681987523000), (1, 1681988787000), (1, 1681988757000), (1, 1681988727000),
                 (1, 1681988546000), (1, 1681988516000), (1, 1681988486000), (1, 1681988456000), (1, 1681987704000),
                 (1, 1681987673000), (1, 1681987643000), (1, 1681987613000), (1, 1681986891000), (1, 1681986861000),
                 (1, 1681986831000), (1, 1681986800000), (1, 1681987012000), (1, 1681986982000), (1, 1681986951000),
                 (1, 1681986921000), (1, 1681987583000), (1, 1681987222000), (1, 1681987192000), (1, 1681987162000),
                 (1, 1681987132000), (1, 1681987343000), (1, 1681987313000), (1, 1681987283000), (1, 1681987252000),
                 (1, 1681987463000), (1, 1681987433000), (1, 1681987403000), (1, 1681987373000), (1, 1681987493000),
                 (1, 1681990502000), (1, 1681990472000), (1, 1681990442000), (1, 1681990412000), (1, 1681990051000),
                 (1, 1681990021000), (1, 1681990623000), (1, 1681990593000), (1, 1681990563000), (1, 1681990533000),
                 (1, 1681987824000), (1, 1681987794000), (1, 1681987764000), (1, 1681987734000), (1, 1681987944000),
                 (1, 1681987914000), (1, 1681987884000), (1, 1681987854000), (1, 1681988907000), (1, 1681988877000),
                 (1, 1681988095000), (1, 1681988305000), (1, 1681988275000), (1, 1681988245000), (1, 1681988215000),
                 (1, 1681988426000), (1, 1681988396000), (1, 1681988366000), (1, 1681990081000), (1, 1681988847000),
                 (1, 1681988817000), (1, 1681990111000), (1, 1681988155000), (1, 1681988125000), (1, 1681989900000),
                 (1, 1681989961000), (1, 1681989931000), (1, 1681988335000), (1, 1681990382000), (1, 1681990352000),
                 (1, 1681990322000), (1, 1681990292000), (1, 1681989991000), (1, 1681988667000), (1, 1681988636000),
                 (1, 1681988606000), (1, 1681988576000), (1, 1681990743000), (1, 1681990713000), (1, 1681990683000),
                 (1, 1681990653000), (1, 1681990864000), (1, 1681990834000), (1, 1681990803000), (1, 1681990773000),
                 (1, 1681990984000), (1, 1681990954000), (1, 1681990924000), (1, 1681990894000), (1, 1681988697000),
                 (1, 1681990202000), (1, 1681990171000), (1, 1681990141000), (1, 1681990232000), (1, 1681990262000),
                 (1, 1681991104000), (1, 1681991074000), (1, 1681991044000), (1, 1681991014000), (1, 1681991225000),
                 (1, 1681991195000), (1, 1681991165000), (1, 1681991135000), (1, 1681991345000), (1, 1681991435000),
                 (1, 1681991405000), (1, 1681991375000), (1, 1681991466000), (1, 1681991556000), (1, 1681991526000),
                 (1, 1681991496000), (1, 1681991706000), (1, 1681991796000), (1, 1681991762000), (1, 1681991734000),
                 (1, 1681991827000), (1, 1681991315000), (1, 1681991285000), (1, 1681991255000), (1, 1681991586000),
                 (1, 1681991676000), (1, 1681991646000), (1, 1681991616000), (1, 1681991856000), (1, 1681991888000),
                 (1, 1681991918000), (1, 1681991948000), (1, 1681991978000), (1, 1681992008000), (1, 1681992038000),
                 (1, 1681992068000), (1, 1681992098000), (1, 1681992128000), (1, 1681992158000), (1, 1681992189000),
                 (1, 1681992279000), (1, 1681992219000), (1, 1681992249000), (1, 1681993452000), (1, 1681992309000),
                 (1, 1681992339000), (1, 1681992369000), (1, 1681992399000), (1, 1681992429000), (1, 1681992459000),
                 (1, 1681992490000), (1, 1681992580000), (1, 1681992520000), (1, 1681992550000), (1, 1681992911000),
                 (1, 1681992610000), (1, 1681992640000), (1, 1681992670000), (1, 1681992760000), (1, 1681992700000),
                 (1, 1681992730000), (1, 1681992790000), (1, 1681992821000), (1, 1681992851000), (1, 1681992881000),
                 (1, 1681992941000), (1, 1681992971000), (1, 1681993001000), (1, 1681993031000), (1, 1681993061000),
                 (1, 1681993091000), (1, 1681993121000), (1, 1681993152000), (1, 1681993182000), (1, 1681993212000),
                 (1, 1681993242000), (1, 1681993272000), (1, 1681993302000), (1, 1681993332000), (1, 1681993362000),
                 (1, 1681993392000), (1, 1681993422000), (1, 1681993482000), (1, 1681993513000), (1, 1681993543000),
                 (1, 1681993573000), (1, 1681993603000), (1, 1681993633000), (1, 1681993663000), (1, 1681993693000),
                 (1, 1681993723000), (1, 1681993753000), (1, 1681993783000), (1, 1681993814000), (1, 1681993844000),
                 (1, 1681993874000), (1, 1681993904000), (1, 1681993934000), (1, 1681993964000), (1, 1681993994000),
                 (1, 1681994024000), (1, 1681994084000), (1, 1681994054000), (1, 1681994265000), (1, 1681994295000),
                 (1, 1681994114000), (1, 1681994145000), (1, 1681994175000), (1, 1681994205000), (1, 1681994235000),
                 (1, 1681994355000), (1, 1681994325000), (1, 1681994385000), (1, 1681994415000), (1, 1681994446000),
                 (1, 1681994476000), (1, 1681994506000), (1, 1681994536000), (1, 1681994566000), (1, 1681994596000),
                 (1, 1681994626000)]

    expected_output = (1204000, 1211000)
    assert tc.calculate_time_values(pya_tuple) == expected_output
