// Generated by CoffeeScript 1.9.2
(function() {
  var get_z_scores, redraw_prob_plot, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  get_z_scores = function(n) {
    var i, j, osm_uniform, ref, x;
    osm_uniform = new Array(n);
    osm_uniform[n - 1] = Math.pow(0.5, 1.0 / n);
    osm_uniform[0] = 1 - osm_uniform[n - 1];
    for (i = j = 1, ref = n - 2; 1 <= ref ? j <= ref : j >= ref; i = 1 <= ref ? ++j : --j) {
      osm_uniform[i] = (i + 1 - 0.3175) / (n + 0.365);
    }
    return (function() {
      var k, len, results;
      results = [];
      for (k = 0, len = osm_uniform.length; k < len; k++) {
        x = osm_uniform[k];
        results.push(jStat.normal.inv(x, 0, 1));
      }
      return results;
    })();
  };

  redraw_prob_plot = function(samples) {
    var container, h, margin, totalh, totalw, w;
    h = 600;
    w = 600;
    margin = {
      left: 60,
      top: 40,
      right: 40,
      bottom: 40,
      inner: 5
    };
    totalh = h + margin.top + margin.bottom;
    totalw = w + margin.left + margin.right;
    container = $("#prob_plot_container");
    container.width(totalw);
    container.height(totalh);
    return nv.addGraph((function(_this) {
      return function() {
        var W, chart, data, names, pvalue, pvalue_str, sample, sorted_names, sorted_values, sw_result, test_str, value, x, z_score;
        chart = nv.models.scatterChart().width(w).height(h).showLegend(false);
        chart.xAxis.axisLabel("Theoretical quantiles").tickFormat(d3.format('.02f'));
        chart.yAxis.axisLabel("Sample quantiles").tickFormat(d3.format('.02f'));
        chart.tooltipContent(function(obj) {
          return '<b style="font-size: 20px">' + obj.point.name + '</b>';
        });
        names = (function() {
          var j, len, ref, results;
          ref = _.keys(samples);
          results = [];
          for (j = 0, len = ref.length; j < len; j++) {
            x = ref[j];
            if (samples[x] !== null) {
              results.push(x);
            }
          }
          return results;
        })();
        sorted_names = names.sort(function(x, y) {
          return samples[x] - samples[y];
        });
        sorted_values = (function() {
          var j, len, results;
          results = [];
          for (j = 0, len = sorted_names.length; j < len; j++) {
            x = sorted_names[j];
            results.push(samples[x]);
          }
          return results;
        })();
        sw_result = ShapiroWilkW(sorted_values);
        W = sw_result.w.toFixed(3);
        pvalue = sw_result.p.toFixed(3);
        pvalue_str = pvalue > 0.05 ? pvalue.toString() : "<span style='color:red'>" + pvalue + "</span>";
        test_str = "Shapiro-Wilk test statistic = " + W + " (p = " + pvalue_str + ")";
        data = [
          {
            slope: jStat.stdev(sorted_values),
            intercept: jStat.mean(sorted_values),
            size: 10,
            values: (function() {
              var j, len, ref, ref1, results;
              ref = _.zip(get_z_scores(sorted_values.length), sorted_values, sorted_names);
              results = [];
              for (j = 0, len = ref.length; j < len; j++) {
                ref1 = ref[j], z_score = ref1[0], value = ref1[1], sample = ref1[2];
                results.push({
                  x: z_score,
                  y: value,
                  name: sample
                });
              }
              return results;
            })()
          }
        ];
        console.log("THE DATA IS:", data);
        d3.select("#prob_plot_container svg").datum(data).call(chart);
        $("#prob_plot_title").html("<h3>Normal probability plot</h3>" + test_str);
        return chart;
      };
    })(this));
  };

  root.redraw_prob_plot_impl = redraw_prob_plot;

}).call(this);
