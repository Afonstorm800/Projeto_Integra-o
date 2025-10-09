"""
Dashboard Module
Visualization of results using Plotly and Flask
"""

import plotly.graph_objects as go
import plotly.express as px
from flask import Flask, render_template_string, jsonify
from typing import Any, Dict, List, Optional, Union
import pandas as pd
from pathlib import Path
import json


class DashboardGenerator:
    """Generate interactive dashboards for data visualization"""
    
    def __init__(self):
        self.figures = []
    
    def create_line_chart(self, data: Union[pd.DataFrame, Dict], 
                         x: str, y: Union[str, List[str]], 
                         title: str = "Line Chart") -> go.Figure:
        """
        Create line chart
        
        Args:
            data: Data as DataFrame or dict
            x: X-axis column name
            y: Y-axis column name(s)
            title: Chart title
            
        Returns:
            Plotly figure
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        if isinstance(y, str):
            y = [y]
        
        fig = go.Figure()
        for y_col in y:
            fig.add_trace(go.Scatter(
                x=data[x],
                y=data[y_col],
                mode='lines+markers',
                name=y_col
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x,
            yaxis_title='Value',
            hovermode='x unified'
        )
        
        return fig
    
    def create_bar_chart(self, data: Union[pd.DataFrame, Dict],
                        x: str, y: str, title: str = "Bar Chart") -> go.Figure:
        """
        Create bar chart
        
        Args:
            data: Data as DataFrame or dict
            x: X-axis column name
            y: Y-axis column name
            title: Chart title
            
        Returns:
            Plotly figure
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        fig = go.Figure(data=[
            go.Bar(x=data[x], y=data[y])
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x,
            yaxis_title=y
        )
        
        return fig
    
    def create_pie_chart(self, data: Union[pd.DataFrame, Dict],
                        labels: str, values: str, 
                        title: str = "Pie Chart") -> go.Figure:
        """
        Create pie chart
        
        Args:
            data: Data as DataFrame or dict
            labels: Column for labels
            values: Column for values
            title: Chart title
            
        Returns:
            Plotly figure
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        fig = go.Figure(data=[
            go.Pie(labels=data[labels], values=data[values])
        ])
        
        fig.update_layout(title=title)
        
        return fig
    
    def create_scatter_plot(self, data: Union[pd.DataFrame, Dict],
                           x: str, y: str, title: str = "Scatter Plot",
                           color: Optional[str] = None) -> go.Figure:
        """
        Create scatter plot
        
        Args:
            data: Data as DataFrame or dict
            x: X-axis column name
            y: Y-axis column name
            title: Chart title
            color: Column for color coding
            
        Returns:
            Plotly figure
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        if color:
            fig = px.scatter(data, x=x, y=y, color=color, title=title)
        else:
            fig = px.scatter(data, x=x, y=y, title=title)
        
        return fig
    
    def create_heatmap(self, data: Union[pd.DataFrame, List[List]], 
                      title: str = "Heatmap",
                      x_labels: Optional[List[str]] = None,
                      y_labels: Optional[List[str]] = None) -> go.Figure:
        """
        Create heatmap
        
        Args:
            data: Data as DataFrame or 2D list
            title: Chart title
            x_labels: X-axis labels
            y_labels: Y-axis labels
            
        Returns:
            Plotly figure
        """
        if isinstance(data, pd.DataFrame):
            x_labels = x_labels or data.columns.tolist()
            y_labels = y_labels or data.index.tolist()
            z_data = data.values
        else:
            z_data = data
        
        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=x_labels,
            y=y_labels,
            colorscale='Viridis'
        ))
        
        fig.update_layout(title=title)
        
        return fig
    
    def create_table(self, data: Union[pd.DataFrame, Dict],
                    title: str = "Data Table") -> go.Figure:
        """
        Create table visualization
        
        Args:
            data: Data as DataFrame or dict
            title: Table title
            
        Returns:
            Plotly figure
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=list(data.columns),
                fill_color='paleturquoise',
                align='left'
            ),
            cells=dict(
                values=[data[col] for col in data.columns],
                fill_color='lavender',
                align='left'
            )
        )])
        
        fig.update_layout(title=title)
        
        return fig
    
    def create_histogram(self, data: Union[pd.DataFrame, Dict, List],
                        column: Optional[str] = None,
                        title: str = "Histogram",
                        bins: int = 30) -> go.Figure:
        """
        Create histogram
        
        Args:
            data: Data as DataFrame, dict, or list
            column: Column name (for DataFrame/dict)
            title: Chart title
            bins: Number of bins
            
        Returns:
            Plotly figure
        """
        if isinstance(data, list):
            values = data
        elif isinstance(data, dict):
            values = data[column]
        else:  # DataFrame
            values = data[column]
        
        fig = go.Figure(data=[
            go.Histogram(x=values, nbinsx=bins)
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=column or 'Value',
            yaxis_title='Frequency'
        )
        
        return fig
    
    def create_box_plot(self, data: Union[pd.DataFrame, Dict],
                       columns: Union[str, List[str]],
                       title: str = "Box Plot") -> go.Figure:
        """
        Create box plot
        
        Args:
            data: Data as DataFrame or dict
            columns: Column name(s) to plot
            title: Chart title
            
        Returns:
            Plotly figure
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        if isinstance(columns, str):
            columns = [columns]
        
        fig = go.Figure()
        for col in columns:
            fig.add_trace(go.Box(y=data[col], name=col))
        
        fig.update_layout(title=title)
        
        return fig
    
    def save_figure(self, fig: go.Figure, filepath: str, format: str = 'html') -> None:
        """
        Save figure to file
        
        Args:
            fig: Plotly figure
            filepath: Output file path
            format: Output format (html, png, jpg, svg)
        """
        if format == 'html':
            fig.write_html(filepath)
        elif format in ['png', 'jpg', 'jpeg', 'svg']:
            fig.write_image(filepath)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def add_figure(self, fig: go.Figure) -> None:
        """Add figure to dashboard collection"""
        self.figures.append(fig)
    
    def generate_dashboard_html(self, output_file: str = "dashboard.html") -> str:
        """
        Generate complete dashboard HTML with all figures
        
        Args:
            output_file: Output file path
            
        Returns:
            HTML content
        """
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="utf-8">',
            '    <title>Data Integration Dashboard</title>',
            '    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>',
            '    <style>',
            '        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }',
            '        h1 { color: #333; text-align: center; }',
            '        .chart-container { background-color: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }',
            '    </style>',
            '</head>',
            '<body>',
            '    <h1>Data Integration Dashboard</h1>',
        ]
        
        for i, fig in enumerate(self.figures):
            div_id = f'chart_{i}'
            html_parts.append(f'    <div class="chart-container"><div id="{div_id}"></div></div>')
        
        html_parts.append('    <script>')
        
        for i, fig in enumerate(self.figures):
            div_id = f'chart_{i}'
            fig_json = fig.to_json()
            html_parts.append(f'        Plotly.newPlot("{div_id}", {fig_json});')
        
        html_parts.extend([
            '    </script>',
            '</body>',
            '</html>'
        ])
        
        html_content = '\n'.join(html_parts)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_content
    
    def create_metrics_card(self, metrics: Dict[str, Any]) -> str:
        """
        Create metrics card HTML
        
        Args:
            metrics: Dictionary of metric names and values
            
        Returns:
            HTML string
        """
        html = '<div class="metrics-container" style="display: flex; flex-wrap: wrap; gap: 20px;">'
        
        for name, value in metrics.items():
            html += f'''
            <div class="metric-card" style="background-color: white; padding: 20px; border-radius: 8px; 
                 box-shadow: 0 2px 4px rgba(0,0,0,0.1); min-width: 200px;">
                <h3 style="margin: 0; color: #666;">{name}</h3>
                <p style="margin: 10px 0 0 0; font-size: 24px; font-weight: bold; color: #333;">{value}</p>
            </div>
            '''
        
        html += '</div>'
        return html


class DashboardServer:
    """Simple Flask server for interactive dashboards"""
    
    def __init__(self, title: str = "Data Integration Dashboard"):
        self.app = Flask(__name__)
        self.title = title
        self.data = {}
        self.charts = {}
        
        @self.app.route('/')
        def index():
            return self.render_dashboard()
        
        @self.app.route('/api/data')
        def get_data():
            return jsonify(self.data)
    
    def add_data(self, name: str, data: Any) -> None:
        """Add data to dashboard"""
        self.data[name] = data
    
    def add_chart(self, name: str, chart: go.Figure) -> None:
        """Add chart to dashboard"""
        self.charts[name] = chart
    
    def render_dashboard(self) -> str:
        """Render dashboard HTML"""
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{self.title}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                h1 {{ color: #333; text-align: center; }}
                .chart-container {{ background-color: white; margin: 20px 0; padding: 20px; 
                                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            </style>
        </head>
        <body>
            <h1>{self.title}</h1>
        '''
        
        for name, chart in self.charts.items():
            html += f'<div class="chart-container"><h2>{name}</h2><div id="chart_{name}"></div></div>'
        
        html += '<script>'
        for name, chart in self.charts.items():
            fig_json = chart.to_json()
            html += f'Plotly.newPlot("chart_{name}", {fig_json});'
        
        html += '</script></body></html>'
        
        return html
    
    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = False) -> None:
        """
        Run dashboard server
        
        Args:
            host: Host address
            port: Port number
            debug: Debug mode
        """
        self.app.run(host=host, port=port, debug=debug)
