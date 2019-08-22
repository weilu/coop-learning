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

  // group by partition
  var partition = [[72], [132, 137, 138, 141, 14, 54], [145, 140, 86], [64, 134], [129, 2, 3, 4, 130, 6, 7, 131, 133, 136, 11, 15, 16, 17, 18, 23, 25, 27, 29, 30, 32, 33, 36, 39, 43, 44, 45, 48, 49, 51, 52, 57, 58, 59, 60, 61, 62, 63, 65, 87, 96, 98, 99, 100, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126], [144, 139, 135], [97, 34, 37, 8, 9, 10, 46, 114, 21, 22, 55, 24, 26, 127, 94, 95], [146], [77], [0, 1, 128, 5, 12, 13, 19, 20, 28, 31, 35, 38, 40, 41, 47, 50, 53, 56, 66, 67, 68, 69, 70, 71, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 85, 88, 89, 90, 91, 92, 93, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113], [42], [142], [143]]
  // shift partition index to skip the first two columns of nodes
  partition = partition.map(coal => coal.map(idx => idx + members.length * 2))

  const partition_link_source = Array(members.length).fill().map((e,i) => i + members.length)
  const partition_link_target = Array(members.length).fill().map((e,i) => i + members.length * 2)
  const partition_link_value = Array(members.length).fill(1)

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
      label: members.concat(members).concat(members).concat(party_list),
      color: colors.concat(colors).concat(colors).concat(group_colors),
      groups: group_values.concat(partition)
    },
    link: {
      source: link_source.concat(partition_link_source),
      target: link_target.concat(partition_link_target),
      value: link_value.concat(partition_link_value)
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
