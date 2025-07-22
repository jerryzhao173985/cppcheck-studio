#!/usr/bin/env node
"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const fs = __importStar(require("fs"));
const generator_1 = require("./generator");
commander_1.program
    .name('cppcheck-dashboard')
    .description('Generate standalone virtual scroll dashboards for CPPCheck analysis results')
    .version('1.0.0')
    .argument('<input>', 'Input JSON file containing CPPCheck analysis results')
    .argument('[output]', 'Output HTML file (default: virtual-dashboard.html)')
    .option('-t, --title <title>', 'Dashboard title', 'CPPCheck Studio - Virtual Scroll Dashboard')
    .option('-p, --project <name>', 'Project name', 'Project')
    .action((input, output) => {
    try {
        // Validate input file exists
        if (!fs.existsSync(input)) {
            console.error(`❌ Error: Input file '${input}' not found`);
            process.exit(1);
        }
        // Determine output file
        const outputFile = output || 'virtual-dashboard.html';
        // Create generator with options
        const generator = new generator_1.VirtualDashboardGenerator(input, {
            title: commander_1.program.opts().title,
            projectName: commander_1.program.opts().project
        });
        // Generate dashboard
        generator.generate(outputFile);
    }
    catch (error) {
        console.error('❌ Error:', error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
commander_1.program.parse();
//# sourceMappingURL=cli.js.map