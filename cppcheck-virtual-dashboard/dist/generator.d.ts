import { GeneratorOptions } from './types';
export declare class VirtualDashboardGenerator {
    private issues;
    private timestamp;
    private options;
    constructor(issuesFile: string, options?: GeneratorOptions);
    generate(outputFile: string): void;
    private calculateStats;
    private generateHTML;
    private generateStyles;
    private generateJavaScript;
}
//# sourceMappingURL=generator.d.ts.map