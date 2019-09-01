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
    Object.keys(exp_partitions).forEach(key => {
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
      width: 1000,
      height: 800,
      font: {
        size: 10
      },
      updatemenus: [{
        active: 0,
        buttons: buttons
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

  var plot_data = ['vi', 'nvi', 'nid'].map(stats_name => {
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

  Plotly.newPlot(`${method_name}_line_plot`, plot_data, layout)
}

Plotly.d3.json("partitions.json", exp_partitions => {
  make_histogram(exp_partitions)
  make_sankey_plot(exp_partitions)

  make_line_plot(exp_partitions, 'k_means')
  make_line_plot(exp_partitions, 'network_block_model_real-normal')
  make_line_plot(exp_partitions, 'network_block_model_discrete-binomial')
})

Plotly.d3.json("partition_reps_nid.json", exp_partitions => {
  make_sankey_plot(exp_partitions, 'nid')
})

Plotly.d3.json("partition_reps_vi.json", exp_partitions => {
  make_sankey_plot(exp_partitions, 'vi')
})
