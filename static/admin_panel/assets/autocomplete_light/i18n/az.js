/*! Select2 4.0.13 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var e;n&&n.fn&&n.fn.select2&&n.fn.select2.amd&&(e=n.fn.select2.amd),e.define("select2/i18n/az",[],function(){return{inputTooLong:function(n){return n.input.length-n.maximum+" simvol silin"},inputTooShort:function(n){return n.minimum-n.input.length+" simvol daxil edin"},loadingMore:function(){return"Daha çox nəticə yüklənir…"},maximumSelected:function(n){return"Sadəcə "+n.maximum+" element seçə bilərsiniz"},noResults:function(){return"Nəticə tapılmadı"},searching:function(){return"Axtarılır…"},removeAllItems:function(){return"Bütün elementləri sil"}}}),e.define,e.require},event=new CustomEvent("dal-language-loaded",{lang:"az"});document.dispatchEvent(event);