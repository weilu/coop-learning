Plotly.d3.json('sankey.json', function(fig){
  const party_list = ["The Jewish Home", "Shas", "United Torah Judaism", "Likud", "Yisrael Beiteinu", "Kulanu", "Yesh Atid", "Zionist Union", "Meretz", "Joint List"]
  const party_colors = d3.schemeRdYlBu[party_list.length]
  const color_fn = d3.scaleOrdinal(party_list, party_colors)
  const node_parties = fig.data[0].node.party
  const colors = node_parties.map(color_fn)

  const members = fig.data[0].node.label
  const link_source = [...Array(members.length).keys()]
  const link_target = Array(members.length).fill().map((e,i)=>i+members.length)
  const link_value = Array(members.length).fill(1)

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
      label: members.concat(members).concat(party_list),
      color: colors.concat(colors).concat(group_colors),
      groups: group_values
    },
    link: {
      source: link_source,
      target: link_target,
      value: link_value
    }
  }

  var data = [data]

  var layout = {
    title: "Knesset Coalition Visualized",
    width: 1200,
    height: 4000,
    font: {
      size: 10
    }
  }

  Plotly.plot('sankey', data, layout)
});
