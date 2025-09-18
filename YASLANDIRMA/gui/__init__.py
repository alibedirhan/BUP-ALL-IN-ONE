#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel İşleme Uygulaması - GUI Package
Modüler GUI yapısını destekleyen paket
"""

# Ana GUI sınıfını import et
from .main_gui import ExcelProcessorGUI

# Tab modüllerini import et
from .file_tab import create_file_processing_tab
from .analysis_tabs import create_analysis_overview_tab, create_arac_detail_tab  
from .other_tabs import create_assignment_tab, create_reports_tab, create_charts_tab

# Yardımcı fonksiyonları import et
from .ui_helpers import (
    ToolTip,
    add_tooltip,
    ProgressManager,
    ThreadedAnalysis,
    show_help_dialog,
    show_about_dialog,
    show_quick_help,
    show_keyboard_shortcuts
)

# Export edilecek sınıf ve fonksiyonlar
__all__ = [
    # Ana sınıf
    'ExcelProcessorGUI',
    
    # Tab oluşturucular
    'create_file_processing_tab',
    'create_analysis_overview_tab',
    'create_arac_detail_tab',
    'create_assignment_tab',
    'create_reports_tab',
    'create_charts_tab',
    
    # Yardımcı sınıflar
    'ToolTip',
    'add_tooltip',
    'ProgressManager',
    'ThreadedAnalysis',
    
    # Dialog fonksiyonları
    'show_help_dialog',
    'show_about_dialog',
    'show_quick_help',
    'show_keyboard_shortcuts'
]

__version__ = "2.0.0-modular"