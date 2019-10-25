function make_sankey_plot(exp_partitions, metric) {
  Plotly.d3.json("sankey.json", fig => {

    const party_list = ["The Jewish Home", "Shas", "United Torah Judaism", "Likud", "Yisrael Beiteinu", "Kulanu", "Yesh Atid", "Zionist Union", "Meretz", "Joint List"]
    const party_colors = d3.schemeRdYlBu[party_list.length + 1]
    const color_fn = d3.scaleOrdinal(party_list, party_colors)
    const node_parties = fig.data[0].node.party
    const colors = node_parties.map(color_fn)

    const members = fig.data[0].node.label.map((l, idx) => idx + ' ' + l)
    const max_group_labels = members.map((_, idx) => 'Coalition ' + (idx + 1))
    const link_source = [...Array(members.length).keys()]
    const link_target = Array(members.length).fill().map((e,i)=>i+members.length)
    const link_value = Array(members.length).fill(1)

    // group by party
    const party_to_member = members.reduce((acc, curr, idx) => {
      party = node_parties[idx]
      if (acc[party] == null) {
        acc[party] = [idx]
      } else {
        acc[party].push(idx)
      }
      return acc
    }, {})
    // TODO: hack plotly.js to preserve order
    const group_values = party_list.map(p => party_to_member[p])
    const group_colors = party_list.map(color_fn)

    const partition_link_source = Array(members.length).fill().map((e,i) => i + members.length)
    const partition_link_target = Array(members.length).fill().map((e,i) => i + members.length * 2)
    const partition_link_value = Array(members.length).fill(1)

    // partition groups
    var partition_tuples = []
    Object.keys(exp_partitions).sort().forEach(key => {
      var partitions = exp_partitions[key]
      partition_tuples = partition_tuples.concat(partitions.map((obj, id) => {
        var p = obj.data
        // shift partition index to skip the first two columns of nodes
        var partition = p.map(coal => coal.map(idx => idx + members.length * 2))
        var partition_name = partitions.length > 1 ?  key + ' partition ' + (id + 1) : key
        return [partition_name, group_values.concat(partition)]
      }))
    })

    var data = {
      type: "sankey",
      orientation: "h",
      node: {
        pad: 15,
        thickness: 15,
        line: {
          color: "black",
          width: 0.5
        },
        label: members.concat(members).concat(members).concat(party_list).concat(max_group_labels),
        color: colors.concat(colors).concat(colors).concat(group_colors),
        groups: partition_tuples[0][1]
      },
      link: {
        source: link_source,
        target: partition_link_target,
        value: link_value,
        label: members,
        color: colors
      }
    }

    var data = [data]

    // generate group by partition buttons
    const buttons = partition_tuples.map(t => {
        return {
            label: t[0],
            method: "restyle",
            args: [
              {
                "node.groups": [t[1]]
              }
            ]
        }
    })

    var title = "Knesset Coalition Visualized"
    if (metric) {
      title = title + `: based on ${metric}`
    }
    var layout = {
      title: title,
      height: 800,
      font: {
        size: 10
      },
      updatemenus: [{
        active: 0,
        buttons: buttons,
        xanchor: 'left',
        yanchor: 'top',
        pad: {'t': -30},
      }]
    }

    if (metric) {
      var el_id = `sankey_reps_${metric}`
    } else {
      var el_id = 'sankey'
    }
    Plotly.plot(el_id, data, layout)
  })
}

function make_histogram(exp_partitions) {
  exp_num_partition_tuples = []
  Object.keys(exp_partitions).forEach(key => {
    var partitions = exp_partitions[key]
    if (partitions.length > 1) {
      var num_partitions = partitions.map(obj => obj.data.length)
      exp_num_partition_tuples.push([key, num_partitions])
    }
  })

  const hist_data = [{
    x: exp_num_partition_tuples[0][1],
    type: 'histogram',
  }]

  const hist_buttons = exp_num_partition_tuples.map(t => {
      return {
          label: t[0],
          method: "restyle",
          args: ["x", [t[1]]]
      }
  })
  const hist_layout = {
    title: "Knesset Coalition Count Histogram",
    font: {
      size: 10
    },
    updatemenus: [{
      active: 0,
      buttons: hist_buttons
    }]
  }
  Plotly.newPlot('histogram', hist_data, hist_layout)
}

function make_line_plot(exp_partitions, method_name) {
  const k_means_keys = Object.keys(exp_partitions)
    .filter(key => key.indexOf(method_name) >= 0)

  var plot_data = ['vi', 'nvi', 'nid', 'nmi', 'ami'].map(stats_name => {
    var x = []
    var y = []
    k_means_keys.forEach(key => {
      var obj = exp_partitions[key][0]
      var stats = obj.stats
      x.push(obj.data.length)
      y.push(stats[stats_name])
    })
    return {
      name: stats_name,
      x: x,
      y: y,
      type: 'scatter'
    }
  })

  var layout = {
    title: `${method_name} clustering quality`,
    xaxis: {
      title: 'Cluster size',
    },
    yaxis: {
      title: 'Value',
    }
  }

  var el_id = `line_plot_${method_name}`
  const el_container = document.getElementById('line_plots')
  el_container.insertAdjacentHTML('afterbegin', `<div id="${el_id}"></div>` )
  Plotly.newPlot(el_id, plot_data, layout)
}

function make_bar_plot(exp_partitions, metric, max_y){
  const x = Object.keys(exp_partitions).sort()
  // const pac_x = x.filter(x => x.indexOf('pac_') >= 0)
  // const non_pac_x = x.filter(x => x.indexOf('pac_') < 0)

  // we want full control over the order of x
  const non_pac_x = ['value_function', 'friends', 'friends_selective', 'enemies_selective', 'enemies', 'boolean']
  const pac_x = non_pac_x.map(x => 'pac_' + x)
  const non_pac_colors = non_pac_x.map(_ => d3.schemeCategory10[0])
  for (var comp_model of ['k_10_means', 'k_2_means', 'network_block_model_auto_B_discrete-geometric_mcmc_sweep_True', 'network_block_model_auto_B_real-normal_mcmc_sweep_True']) {
    non_pac_x.push(comp_model)
    non_pac_colors.push(d3.schemeCategory10[2])
  }
  console.log(non_pac_x)
  const x_labels = [
    'Value Function', 'Friends', 'Selective Friends', 'Selective Enemies', 'Enemies', 'Boolean',
    'k-means (k=10)', 'k-means (k=2)', 'SBM Geometric', 'SBM Normal'
  ]

  function get_y(key) {
    return exp_partitions[key][0].stats[metric]
  }
  const pac_y = pac_x.map(get_y)
  const non_pac_y = non_pac_x.map(get_y)

  const pac_data = {
    y: x_labels,
    x: pac_y,
    text: pac_y.map(n => n.toFixed(2)),
    textposition: "outside",
    type: 'bar',
    orientation: 'h',
    name: 'PAC'
  }
  const non_pac_data = {
    y: x_labels,
    x: non_pac_y,
    text: non_pac_y.map(n => n.toFixed(2)),
    textposition: "outside",
    type: 'bar',
    orientation: 'h',
    name: 'Full Info',
    marker:{
      color: non_pac_colors
    },
  }

  var layout = {
    title: `Model ${metric} values`,
    height: 700,
    font: { size: 10 },
    barmode: 'group',
    xaxis: {
      automargin: true
    },
    yaxis: {
      automargin: true,
      autorange: 'reversed'
    }
  }

  Plotly.newPlot(`bar_reps_${metric}`, [non_pac_data, pac_data], layout);
}


Plotly.d3.json("partitions.json", exp_partitions => {
  make_histogram(exp_partitions)
  make_sankey_plot(exp_partitions)

  make_line_plot(exp_partitions, 'k_means')
})

function create_sankey_and_bar_el(metric) {
  const el_container = document.getElementById('sankeys')
  el_container.insertAdjacentHTML('beforeend', `<div class="row"><div id="sankey_reps_${metric}"></div><div id="bar_reps_${metric}"></div></div>`)
}

Plotly.d3.json("partition_reps_vi.json", exp_partitions => {
  var metric = 'vi'
  create_sankey_and_bar_el(metric)
  make_sankey_plot(exp_partitions, metric)
  make_bar_plot(exp_partitions, metric)

  var metric = 'ami'
  create_sankey_and_bar_el(metric)
  make_bar_plot(exp_partitions, metric)
})
