// Generated by CoffeeScript 1.3.3
(function() {

  $(function() {
    var Chromosome, Manhattan_Plot, Permutation_Histogram, sort_number;
    sort_number = function(a, b) {
      return a - b;
    };
    Permutation_Histogram = (function() {

      function Permutation_Histogram() {
        this.process_data();
        this.display_graph();
      }

      Permutation_Histogram.prototype.process_data = function() {
        var bars, floored, key, keys, lrs, lrs_array, _i, _j, _len, _len1;
        lrs_array = js_data.lrs_array;
        bars = {};
        for (_i = 0, _len = lrs_array.length; _i < _len; _i++) {
          lrs = lrs_array[_i];
          floored = Math.floor(lrs);
          if (!(floored in bars)) {
            bars[floored] = 0;
          }
          bars[floored] += 1;
        }
        keys = [];
        for (key in bars) {
          keys.push(key);
        }
        keys.sort(sort_number);
        this.bars_ordered = [];
        for (_j = 0, _len1 = keys.length; _j < _len1; _j++) {
          key = keys[_j];
          this.bars_ordered.push([parseInt(key), bars[key]]);
        }
        console.log("bars is:", bars);
        console.log("keys are:", keys);
        return console.log("bars_ordered are:", this.bars_ordered);
      };

      Permutation_Histogram.prototype.display_graph = function() {
        return $.jqplot('permutation_histogram', [this.bars_ordered], {
          title: 'Permutation Histogram',
          seriesDefaults: {
            renderer: $.jqplot.BarRenderer,
            rendererOptions: {
              barWidth: 15
            },
            pointLabels: {
              show: true
            }
          },
          axesDefaults: {
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer
          },
          axes: {
            xaxis: {
              min: 0,
              label: "LRS",
              pad: 1.1
            },
            yaxis: {
              min: 0,
              label: "Frequency"
            }
          }
        });
      };

      return Permutation_Histogram;

    })();
    Chromosome = (function() {

      function Chromosome(name) {
        this.name = name;
        this.max_mb = 0;
        this.plot_points = [];
      }

      Chromosome.prototype.process_point = function(mb, lrs) {
        if (mb > this.max_mb) {
          this.max_mb = mb;
        }
        return this.plot_points.push([mb, lrs]);
      };

      Chromosome.prototype.display_graph = function() {
        var div_name, x_axis_max, x_axis_ticks, x_tick;
        div_name = 'manhattan_plot_' + this.name;
        console.log("div_name:", div_name);
        x_axis_max = Math.ceil(this.max_mb / 25) * 25;
        x_axis_ticks = [];
        x_tick = 0;
        while (x_tick <= x_axis_max) {
          x_axis_ticks.push(x_tick);
          x_tick += 25;
        }
        return $.jqplot(div_name, [this.plot_points], {
          title: this.name,
          seriesDefaults: {
            showLine: false,
            markerRenderer: $.jqplot.MarkerRenderer,
            markerOptions: {
              style: "filledCircle",
              size: 3
            }
          },
          axesDefaults: {
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer
          },
          axes: {
            xaxis: {
              min: 0,
              max: x_axis_max,
              ticks: x_axis_ticks,
              tickOptions: {
                angle: 90,
                showGridline: false,
                formatString: '%d'
              },
              label: "Megabases"
            },
            yaxis: {
              min: 0,
              label: "LRS",
              tickOptions: {
                showGridline: false
              }
            }
          }
        });
      };

      return Chromosome;

    })();
    Manhattan_Plot = (function() {

      function Manhattan_Plot() {
        this.chromosomes = {};
        this.build_chromosomes();
        this.display_graphs();
      }

      Manhattan_Plot.prototype.build_chromosomes = function() {
        var chromosome, mb, result, _i, _len, _ref, _results;
        _ref = js_data.qtl_results;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          result = _ref[_i];
          chromosome = result.locus.chromosome;
          if (!(chromosome in this.chromosomes)) {
            this.chromosomes[chromosome] = new Chromosome(chromosome);
          }
          mb = parseInt(result.locus.mb);
          _results.push(this.chromosomes[chromosome].process_point(mb, result.lrs));
        }
        return _results;
      };

      Manhattan_Plot.prototype.display_graphs = function() {
        /* Call display_graph for each chromosome
        */

        var extra_keys, html, key, keys, numbered_keys, _i, _len, _results;
        numbered_keys = [];
        extra_keys = [];
        for (key in this.chromosomes) {
          if (isNaN(key)) {
            extra_keys.push(key);
          } else {
            numbered_keys.push(key);
          }
        }
        numbered_keys.sort(sort_number);
        extra_keys.sort();
        keys = numbered_keys.concat(extra_keys);
        console.log("keys are:", keys);
        _results = [];
        for (_i = 0, _len = keys.length; _i < _len; _i++) {
          key = keys[_i];
          html = "<div id=\"manhattan_plot_" + key + "\" class=\"manhattan_plot_segment\"></div>";
          console.log("html is:", html);
          $("#manhattan_plots").append(html);
          _results.push(this.chromosomes[key].display_graph());
        }
        return _results;
      };

      return Manhattan_Plot;

    })();
    new Permutation_Histogram;
    return new Manhattan_Plot;
  });

}).call(this);
