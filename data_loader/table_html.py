def table_html(district, palika, ward, return_q, pcr_p, rdt_p, return_nq, pcr_n, rdt_n, return_t, pcr_t, rdt_t):
  return ("""<style type="text/css">
  .tg  {border-collapse:collapse;border-spacing:0;}
  .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
    overflow:hidden;padding:10px 5px;word-break:normal;}
  .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
    font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
  .tg .tg-x5oc{background-color:#fe996b;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-0cjc{background-color:#67fd9a;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-266k{background-color:#9b9b9b;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-d52n{background-color:#32cb00;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-7od5{background-color:#9aff99;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-y698{background-color:#efefef;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-tw5s{background-color:#fe0000;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-pidv{background-color:#ffce93;border-color:inherit;text-align:left;vertical-align:top}
  </style>
  <table class="tg">
  <thead>
    <tr>
      <th class="tg-y698" colspan="2">District</th>
      <th class="tg-y698" colspan="3">"""+str(district)+"""</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="tg-0pky" colspan="2">Palika</td>
      <td class="tg-0pky" colspan="3">"""+str(palika)+"""</td>
    </tr>
    <tr>
      <td class="tg-y698" colspan="2">Ward No</td>
      <td class="tg-y698" colspan="3">"""+str(ward)+"""</td>
    </tr>
    <tr>
      <td class="tg-266k" colspan="2">Returnee</td>
      <td class="tg-266k">Test</td>
      <td class="tg-266k">PCR</td>
      <td class="tg-266k">RDT</td>
    </tr>
    <tr>
      <td class="tg-7od5">Quarantined</td>
      <td class="tg-7od5">"""+str(return_q)+"""</td>
      <td class="tg-tw5s">Positive</td>
      <td class="tg-tw5s">"""+str(pcr_p)+"""</td>
      <td class="tg-x5oc">"""+str(rdt_p)+"""</td>
    </tr>
    <tr>
      <td class="tg-pidv">Not-Quarentined</td>
      <td class="tg-pidv">"""+str(return_nq)+"""</td>
      <td class="tg-d52n">Negative</td>
      <td class="tg-d52n">"""+str(pcr_n)+"""</td>
      <td class="tg-0cjc">"""+str(rdt_n)+"""</td>
    </tr>
    <tr>
      <td class="tg-y698">Total</td>
      <td class="tg-y698">"""+str(return_t)+"""</td>
      <td class="tg-y698">Total</td>
      <td class="tg-y698">"""+str(pcr_t)+"""</td>
      <td class="tg-y698">"""+str(rdt_t)+"""</td>
    </tr>
  </tbody>
  </table>""")

def table_return_html(district, palika, ward, return_t, color):
  return ("""<style type="text/css">
  .tg  {border-collapse:collapse;border-spacing:0;}
  .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
    overflow:hidden;padding:10px 5px;word-break:normal;}
  .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
    font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
  .tg .tg-x5oc{background-color:#fe996b;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-0cjc{background-color:#67fd9a;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-266k{background-color:#9b9b9b;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-266ka{background-color:"""+color+""";border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-d52n{background-color:#32cb00;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-7od5{background-color:#9aff99;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-y698{background-color:#efefef;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-tw5s{background-color:#fe0000;border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-pidv{background-color:#ffce93;border-color:inherit;text-align:left;vertical-align:top}
  </style>
  <table class="tg">
  <thead>
    <tr>
      <th class="tg-y698" colspan="2">District</th>
      <th class="tg-y698" colspan="3">"""+str(district)+"""</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="tg-0pky" colspan="2">Palika</td>
      <td class="tg-0pky" colspan="3">"""+str(palika)+"""</td>
    </tr>
    <tr>
      <td class="tg-y698" colspan="2">Ward No</td>
      <td class="tg-y698" colspan="3">"""+str(ward)+"""</td>
    </tr>
    <tr>
      <td class="tg-266k" colspan="2">Returnee</td>
      <td class="tg-266ka" colspan="3">"""+str(return_t)+"""</td>
    </tr>
  </tbody>
  </table>""")