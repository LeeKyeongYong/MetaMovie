<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="ko">
	<%@ include file="./include/head.jsp"%>
<body>
    <!-- Page Preloder -->
    <div id="preloder">
        <div class="loader"></div>
    </div>
  <!-- header -->
	<%@ include file="./header.jsp"%>
    <!-- Breadcrumb Begin -->
	<%@ include file="./include/BreadcurmbList.jsp"%>
    <!-- Breadcrumb End -->
    <!-- Product Section Begin -->
    <section class="product-page spad">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <div class="product__page__content">
                        <div class="product__page__title">
                            <div class="row">
                                <div class="col-lg-8 col-md-8 col-sm-6">
                                    <div class="section-title">
                                        <h4>박스오피스</h4>
                                    </div>
                                </div>
                                <div class="col-lg-4 col-md-4 col-sm-6">
                                    <div class="product__page__filter">
                                        <p>날짜별 검색</p>
                                        	<div class="nice-selects">
                                        		<input type="text" id="dateSelect"/>
                                        	</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row" id="rowproduct">
                        </div>
					</div>
				</div>
		   </div>
		</div>
</section>
<!-- Product Section End -->

<!-- footer section -->
		<%@ include file="./footer.jsp"%>

  <!-- Search model Begin -->
	<%@ include file="./search.jsp"%>
<!-- Search model end -->
<%@ include file="./include/jsscript.jsp"%>
	<!-- Js Plugins -->
	<script>
	$( function() {
		var myDate  = new Date();
		var prettyDate = new Date(myDate.setDate(myDate.getDate() - 1));	// 어제
		var yesterdate = prettyDate.getFullYear()+'-'+(prettyDate.getMonth()+1) + '-' +(prettyDate.getDate()<10?'0'+prettyDate.getDate():prettyDate.getDate());
		showList(yesterdate);
		$.datepicker.regional['ko'] = {
	           monthNames: ['1월(JAN)','2월(FEB)','3월(MAR)','4월(APR)','5월(MAY)','6월(JUN)','7월(JUL)','8월(AUG)','9월(SEP)','10월(OCT)','11월(NOV)','12월(DEC)'],
	            monthNamesShort: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
	            dayNames: ['일','월','화','수','목','금','토'],
	            dayNamesShort: ['일','월','화','수','목','금','토'],
	            dayNamesMin: ['일','월','화','수','목','금','토'],
	            weekHeader: 'Wk',
	            dateFormat: 'yy-mm-dd',
	            showMonthAfterYear: true,
	            yearSuffix: '',
	            changeMonth: true,
	            changeYear: true,
	            yearRange: 'c-99:c+99'
	        };
	    $.datepicker.setDefaults($.datepicker.regional['ko']);
		$("#dateSelect").datepicker();
		 $("#dateSelect").val(yesterdate); 
		 $('#dateSelect').datepicker("option", "maxDate",yesterdate);
		 $('#dateSelect').on("change", function() {
			 $("#rowproduct").empty();
			 showList(this.value);
		 });
	  });
	function showList(date){
		var key = "f9a5e15b3b0e1e90e656e39bf714f0a3";
		var api_key = "9d58f50eea3bc0cebe233c422bbef69e";
        var apiUrl = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key="+key+"&targetDt="+date.replaceAll(/-/gi,"");
        const rowproduct = document.querySelector('#rowproduct');
        const xhr = new XMLHttpRequest();
        
        xhr.onreadystatechange = function(){
        	 if(xhr.readyState == 4 && xhr.status == 200){
        		 var jsonObj = JSON.parse(xhr.response);
        		 const boxOfficeResult = jsonObj['boxOfficeResult'];
        		 const movieList = boxOfficeResult['dailyBoxOfficeList'];
        		 movieList.forEach(element => {
        			 var searchUrl = "https://api.themoviedb.org/3/search/movie?api_key="+api_key+"&language=ko-Kr&page=1&include_adult=false&query="+element['movieNm'];
        			 var base_url = "https://image.tmdb.org/t/p/w300/";
        			 const myDiv = document.createElement('div');
        			 fetch(searchUrl).then(res => res.json()).then(function(res){
                    	myDiv.classList.add('col-lg-3');
                    	myDiv.classList.add('col-md-5');
                    	myDiv.classList.add('col-sm-5');
                    var output="<div class='product__item'>";
                    	 output+= "<a href='RankingDetails.do?cmt_seq="+res.results[0].id+"&movie_seq="+element['movieCd']+"&movie_title="+res.results[0].title+"'>";
                    	 output+= "<div class='product__item__pic set-bg' data-setbg='"+base_url+res.results[0].poster_path+"' style='background-image: url("+(base_url+res.results[0].poster_path)+");'>";
                    	 output+="<div class='comment'><i class='fa fa-star'></i>&nbsp;&nbsp; "+res.results[0].vote_average;
                    	 output+="</div> <div class='view'><i class='fa fa-upload'></i>&nbsp;&nbsp;"+res.results[0].release_date+"</div></div>";
                    	 output+="<div class='product__item__text'> <h5>"+res.results[0].title+"</a></h5></div></div>";
                    	 myDiv.innerHTML=output;
                    	 rowproduct.appendChild(myDiv);
                     }).catch(error => console.log(error));
                 });
        	 }
        }
        xhr.open('GET', apiUrl, true);
        xhr.send();
	}
	</script>
</body>
</html>