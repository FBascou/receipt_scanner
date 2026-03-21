import * as d3 from "d3";

export interface LineChartOptions<T> {
  selector: string;
  data: T[];
  x: (d: T) => string | Date;
  y: (d: T) => number;
  width?: number;
  height?: number;
}

export function renderLineChart<T>({
  selector,
  data,
  x,
  y,
  width = 300,
  height = 200,
}: LineChartOptions<T>) {
  const parseDate = d3.timeParse("%Y-%m-%d");

  // Normalize data
  const normalizedData = data.map((d) => ({
    raw: d,
    date: typeof x(d) === "string" ? parseDate(x(d) as string)! : (x(d) as Date),
    value: +y(d), // Important: coerce to number
  }));

  const margin = { top: 20, right: 20, bottom: 20, left: 40 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const svg = d3
    .select(selector)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // X scale (time)
  const xScale = d3
    .scaleTime()
    .domain(d3.extent(normalizedData, (d) => d.date) as [Date, Date])
    .range([0, innerWidth]);

  // Y scale (linear)
  const yScale = d3
    .scaleLinear()
    .domain(d3.extent(normalizedData, (d) => d.value) as [number, number])
    .nice()
    .range([innerHeight, 0]);

  // Axes
  const xAxis = d3
    .axisBottom<Date>(xScale)
    .ticks(5)
    .tickFormat((d: Date | number) => (d instanceof Date ? d3.timeFormat("%Y-%m-%d")(d) : ""));

  svg.append("g").attr("transform", `translate(0,${innerHeight})`).call(xAxis);

  const yAxis = d3
    .axisLeft<number>(yScale)
    .ticks(5)
    .tickFormat((d) => `$${d}`);

  svg.append("g").call(yAxis);

  // Line
  const line = d3
    .line<(typeof normalizedData)[number]>()
    .x((d) => xScale(d.date))
    .y((d) => yScale(d.value));

  svg
    .append("path")
    .datum(normalizedData)
    .attr("fill", "none")
    .attr("stroke", "var(--clr-accent)")
    .attr("stroke-width", 2)
    .attr("d", line);

  // Tooltip
  const tooltip = d3.select(selector).append("div").attr("class", "tooltip");

  svg
    .selectAll("circle")
    .data(normalizedData)
    .enter()
    .append("circle")
    .attr("cx", (d) => xScale(d.date))
    .attr("cy", (d) => yScale(d.value))
    .attr("r", 4)
    .attr("fill", "var(--clr-accent)")
    .on("mouseenter", (_, d) => {
      tooltip.style("opacity", "1").html(`
          <strong>Date:</strong> ${d3.timeFormat("%Y-%m-%d")(d.date)}<br/>
          <strong>Amount:</strong> $${d.value.toFixed(2)}
        `);
    })
    .on("mousemove", (event) => {
      tooltip.style("left", event.pageX + 12 + "px").style("top", event.pageY - 28 + "px");
    })
    .on("mouseleave", () => {
      tooltip.style("opacity", "0");
    });

  // console.log(normalizedData.map((d) => ({ date: d.date, value: d.value })));
  // console.log("X domain:", xScale.domain());
  // console.log("Y domain:", yScale.domain());
}
