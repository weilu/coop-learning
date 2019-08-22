Plotly.d3.json("sankey.json", fig => {
Plotly.d3.json("partitions.json", exp_partitions => {

  const party_list = ["The Jewish Home", "Shas", "United Torah Judaism", "Likud", "Yisrael Beiteinu", "Kulanu", "Yesh Atid", "Zionist Union", "Meretz", "Joint List"]
  const party_colors = d3.schemeRdYlBu[party_list.length]
  const color_fn = d3.scaleOrdinal(party_list, party_colors)
  const node_parties = fig.data[0].node.party
  const colors = node_parties.map(color_fn)

  const members = fig.data[0].node.label
  const link_source = [...Array(members.length).keys()]
  const link_target = Array(members.length).fill().map((e,i)=>i+members.length)
  const link_value = Array(members.length).fill(1)

  const dummy_labels = Array(members.length).fill('')

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
    partition_tuples = partition_tuples.concat(partitions.map((p, id) => {
      // shift partition index to skip the first two columns of nodes
      var partition = p.map(coal => coal.map(idx => idx + members.length * 2))
      var partition_name = key + ' partition ' + (id + 1)
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
      label: dummy_labels.concat(members).concat(dummy_labels).concat(party_list),
      color: dummy_labels.concat(colors).concat(dummy_labels).concat(group_colors),
      groups: partition_tuples[0][1]
    },
    link: {
      source: link_source.concat(partition_link_source),
      target: link_target.concat(partition_link_target),
      value: link_value.concat(partition_link_value)
    }
  }

  var data = [data]

  // generate group by partition buttons
  const buttons = partition_tuples.map(t => {
      return {
          label: t[0],
          method: "restyle",
          args: ["node.groups", [t[1]]]
      }
  })

  var layout = {
    title: "Knesset Coalition Visualized",
    width: 1200,
    height: 4000,
    font: {
      size: 10
    },
    updatemenus: [{
      active: 0,
      buttons: buttons
    }]
  }

  Plotly.plot('sankey', data, layout)
})
})
