<h1>GMO yours auto-booking</h1>
<h2>Introduction</h2>
<p>
  GMOインターネットグループのランチビュッフェ「<a href="https://esp03.dt-r.com/gmo-yours/">GMO yours</a>」のPythonによる当日自動予約ツールです。<br>
  <a href="http://direct-reserve.info/">Direct Reserve</a>社のサービスを利用しているため、同社提供のサービスをスクレイピングしたい方も参考になるかと思います。
<h2>How to use</h2>
<p>
  <ol>
    <li>Python,Selenium,ChromeDriverの実行環境をご用意ください。別のWeb Driverを利用したい場合、pyファイルのWeb Driver設定の部分を修正することで使用できるようになるかと思います。</li>
    <li>(ChromeDriver使用者のみ)yours.pyの22行目の「ENTER YOUR CHROMEDRIVE PATH」にご自身のchromedriverのpathを入力してください。</li>
    <li>当日分しか予約ができないため、0時以降にご使用ください。また当日の予約ができる11時以降になると自動で処理が終了します。</li>
    <li>他の予約が無い状態でご使用ください。以下に記載する通り、処理内容が理由となります。</li>
  </ol>
</p>
<h2>About processing</h2>
<p>
  予約は①12:00-12:10②12:10-12:20③12:20-12:30④13:00-13:10⑤13:10-13:20⑥13:20-13:30の6つの枠があり、①と④を「00枠」、②と⑤を「10枠」、③と⑥を「20枠」と呼んでいました。<br>
  本ツールでは取得する予約枠を「00枠」と「10枠」に限定しています(20枠は既におかずがなくなっている可能性が生じるため)。<br>
  更に優先的に「00枠」を取得するため、「00枠」で予約できた場合には処理が終了しますが、「10枠」で予約した場合には再度自動予約ループに戻り、「00枠」に限定して予約する仕様になっております。<br>
  「10枠」を予約した後に「00枠」を予約できた場合には、「10枠」を自動でキャンセルする処理もプログラムに書かれています。<br>
  そのため一時的にではありますが2つの枠を同時に予約し得るので、最大予約数が2である当予約システムにおいて本ツールを使用する際には、別の予約をキャンセルしてからのご使用を推奨しています。<br>
</p>
<h2>License</h2>
<p>
  自己責任で。それ以外はどう使ってくれてもなんでもいいです。
</p>
